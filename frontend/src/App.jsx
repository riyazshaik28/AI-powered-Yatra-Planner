import { useEffect, useMemo, useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
const EVENTS = [
  ["start", "Preparing your trip"],
  ["weather", "Checking the forecast"],
  ["weather_complete", "Weather ready"],
  ["places_complete", "Places ready"],
  ["currency_complete", "Currency ready"],
  ["complete", "Plan complete"],
];

const initialForm = {
  destination: "Delhi",
  start_date: "",
  end_date: "",
  base_currency: "INR",
};

function today(offset = 0) {
  const date = new Date();
  date.setDate(date.getDate() + offset);
  return date.toISOString().slice(0, 10);
}

function readSavedTrips() {
  try {
    return JSON.parse(localStorage.getItem("yatra-saved-trips") || "[]");
  } catch {
    return [];
  }
}

function App() {
  const [form, setForm] = useState({ ...initialForm, start_date: today(1), end_date: today(4) });
  const [status, setStatus] = useState("idle");
  const [activeEvent, setActiveEvent] = useState("");
  const [message, setMessage] = useState("");
  const [weather, setWeather] = useState([]);
  const [places, setPlaces] = useState([]);
  const [rates, setRates] = useState({});
  const [placeFilter, setPlaceFilter] = useState("All");
  const [savedTrips, setSavedTrips] = useState(readSavedTrips);
  const [error, setError] = useState("");

  useEffect(() => {
    localStorage.setItem("yatra-saved-trips", JSON.stringify(savedTrips));
  }, [savedTrips]);

  const categories = useMemo(
    () => ["All", ...new Set(places.map((place) => place.category))],
    [places],
  );
  const filteredPlaces = places.filter(
    (place) => placeFilter === "All" || place.category === placeFilter,
  );
  const completedSteps = EVENTS.findIndex(([event]) => event === activeEvent);

  function updateField(event) {
    setForm((current) => ({ ...current, [event.target.name]: event.target.value }));
  }

  async function generatePlan(event) {
    event.preventDefault();
    setStatus("loading");
    setActiveEvent("start");
    setError("");
    setMessage("");
    setWeather([]);
    setPlaces([]);
    setRates({});

    try {
      const response = await fetch(`${API_URL}/stream`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "text/event-stream" },
        body: JSON.stringify(form),
      });
      if (!response.ok) {
        const detail = await response.json().catch(() => ({}));
        throw new Error(detail.detail || "Unable to generate this trip.");
      }
      if (!response.body) throw new Error("The server returned an empty stream.");

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";
      while (true) {
        const { value, done } = await reader.read();
        buffer += decoder.decode(value || new Uint8Array(), { stream: !done });
        const chunks = buffer.split("\n\n");
        buffer = chunks.pop() || "";
        for (const chunk of chunks) {
          const eventName = chunk.match(/^event: (.+)$/m)?.[1];
          const dataLine = chunk.match(/^data: (.+)$/m)?.[1];
          if (!eventName || !dataLine) continue;
          const data = JSON.parse(dataLine);
          setActiveEvent(eventName);
          if (eventName === "weather_complete") setWeather(data.data || []);
          if (eventName === "places_complete") setPlaces(data.data || []);
          if (eventName === "currency_complete") setRates(data.data || {});
          if (eventName === "error") throw new Error(data.error || "Trip generation failed.");
          setMessage(data.message || "");
        }
        if (done) break;
      }
      setStatus("complete");
    } catch (generationError) {
      setStatus("error");
      setError(generationError.message);
    }
  }

  function saveTrip() {
    const trip = {
      id: Date.now(),
      destination: form.destination,
      start_date: form.start_date,
      end_date: form.end_date,
      places: places.length,
      savedAt: new Date().toLocaleDateString(),
    };
    setSavedTrips((current) => [trip, ...current.filter((item) => item.destination !== trip.destination)]);
  }

  function loadTrip(trip) {
    setForm((current) => ({ ...current, destination: trip.destination, start_date: trip.start_date, end_date: trip.end_date }));
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  return (
    <div className="min-h-screen">
      <header className="mx-auto flex max-w-6xl items-center justify-between px-6 py-6">
        <div className="flex items-center gap-3">
          <div className="grid h-11 w-11 place-items-center rounded-2xl bg-ink text-xl text-white shadow-lg shadow-slate-300">✦</div>
          <div><div className="text-lg font-bold tracking-tight">Yatra</div><div className="text-xs text-slate-500">travel, thoughtfully planned</div></div>
        </div>
        <div className="rounded-full border border-slate-200 bg-white/70 px-4 py-2 text-sm text-slate-600">✈ Live trip planner</div>
      </header>

      <main className="mx-auto max-w-6xl px-6 pb-16">
        <section className="grid items-end gap-10 pb-12 pt-12 lg:grid-cols-[1.1fr_0.9fr]">
          <div>
            <p className="mb-4 text-sm font-bold uppercase tracking-[0.22em] text-coral">Your next story starts here</p>
            <h1 className="serif max-w-xl text-5xl leading-[1.04] text-ink sm:text-6xl">A better trip, <span className="text-coral">beautifully</span> planned.</h1>
            <p className="mt-6 max-w-lg text-lg leading-8 text-slate-600">Bring a destination and a few dates. We&apos;ll bring the forecast, places worth seeing, and the right currency in one calm itinerary.</p>
          </div>
          <div className="rounded-[2rem] bg-ink p-7 text-white shadow-2xl shadow-slate-300">
            <div className="mb-6 flex items-center justify-between"><span className="text-sm text-slate-300">Start planning</span><span className="text-2xl">☼</span></div>
            <form onSubmit={generatePlan} className="space-y-4">
              <label className="block text-sm text-slate-300">Where are you going?
                <input required name="destination" value={form.destination} onChange={updateField} className="mt-2 w-full rounded-xl border border-slate-600 bg-slate-800 px-4 py-3 text-white outline-none ring-coral focus:ring-2" placeholder="Try Delhi, Mumbai..." />
              </label>
              <div className="grid grid-cols-2 gap-3">
                <label className="text-sm text-slate-300">From<input required type="date" name="start_date" value={form.start_date} onChange={updateField} className="mt-2 w-full rounded-xl border border-slate-600 bg-slate-800 px-3 py-3 text-white outline-none focus:ring-2 focus:ring-coral" /></label>
                <label className="text-sm text-slate-300">To<input required type="date" name="end_date" value={form.end_date} onChange={updateField} className="mt-2 w-full rounded-xl border border-slate-600 bg-slate-800 px-3 py-3 text-white outline-none focus:ring-2 focus:ring-coral" /></label>
              </div>
              <label className="block text-sm text-slate-300">Currency
                <select name="base_currency" value={form.base_currency} onChange={updateField} className="mt-2 w-full rounded-xl border border-slate-600 bg-slate-800 px-4 py-3 text-white outline-none focus:ring-2 focus:ring-coral"><option>INR</option><option>USD</option><option>EUR</option><option>GBP</option></select>
              </label>
              <button disabled={status === "loading"} className="w-full rounded-xl bg-coral px-4 py-3.5 font-bold text-white transition hover:bg-orange-500 disabled:cursor-wait disabled:opacity-60">{status === "loading" ? "Building your trip..." : "Build my trip  →"}</button>
            </form>
          </div>
        </section>

        {error && <div className="mb-8 rounded-2xl border border-red-200 bg-red-50 p-4 text-red-700">Couldn&apos;t build the trip: {error}</div>}
        <section className="mb-10 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="mb-5 flex items-center justify-between"><div><p className="text-xs font-bold uppercase tracking-widest text-slate-400">Live progress</p><h2 className="mt-1 text-xl font-bold">Your trip is coming together</h2></div><span className="text-sm text-slate-500">{status === "complete" ? "Ready to explore" : message || "Waiting for your dates"}</span></div>
          <div className="grid gap-3 sm:grid-cols-3 lg:grid-cols-6">
            {EVENTS.map(([event, label], index) => <div key={event} className={`rounded-2xl p-3 ${index <= completedSteps ? "bg-orange-50 text-coral" : "bg-slate-50 text-slate-400"}`}><div className="mb-2 text-lg">{index <= completedSteps ? "✓" : "○"}</div><div className="text-xs font-semibold">{label}</div></div>)}
          </div>
        </section>

        {status === "complete" && <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
          <section className="rounded-3xl bg-white p-6 shadow-sm ring-1 ring-slate-100">
            <div className="mb-5 flex items-center justify-between"><div><p className="text-xs font-bold uppercase tracking-widest text-coral">The forecast</p><h2 className="mt-1 text-2xl font-bold">{form.destination} weather</h2></div><span className="rounded-full bg-orange-50 px-3 py-1 text-xs font-bold text-orange-600">{weather.length} days</span></div>
            <div className="grid gap-3 sm:grid-cols-2">{weather.map((day) => <div key={day.date} className="flex items-center justify-between rounded-2xl bg-slate-50 p-4"><div><div className="font-bold">{day.condition}</div><div className="mt-1 text-xs text-slate-500">{day.date} · {day.humidity}% humidity</div></div><div className="text-right"><div className="font-bold text-coral">{Math.round(day.temperature_high)}°</div><div className="text-xs text-slate-400">{Math.round(day.temperature_low)}° low</div></div></div>)}</div>
          </section>
          <section className="rounded-3xl bg-ink p-6 text-white shadow-sm"><p className="text-xs font-bold uppercase tracking-widest text-slate-400">Currency snapshot</p><h2 className="mt-1 text-2xl font-bold">Rates in {form.base_currency}</h2><p className="mt-2 text-sm text-slate-400">A quick reference for your trip budget.</p><div className="mt-6 grid grid-cols-2 gap-3">{Object.entries(rates).slice(0, 6).map(([currency, value]) => <div key={currency} className="rounded-2xl bg-white/10 p-3"><div className="text-xs text-slate-400">{currency}</div><div className="mt-1 font-bold">{Number(value).toFixed(2)}</div></div>)}</div></section>
        </div>}

        {places.length > 0 && <section className="mt-6 rounded-3xl bg-white p-6 shadow-sm ring-1 ring-slate-100"><div className="flex flex-wrap items-end justify-between gap-4"><div><p className="text-xs font-bold uppercase tracking-widest text-coral">Go a little further</p><h2 className="mt-1 text-2xl font-bold">Places to make it memorable</h2></div><div className="flex gap-2 overflow-x-auto">{categories.map((category) => <button onClick={() => setPlaceFilter(category)} key={category} className={`whitespace-nowrap rounded-full px-3 py-1.5 text-xs font-bold ${placeFilter === category ? "bg-ink text-white" : "bg-slate-100 text-slate-500"}`}>{category}</button>)}</div></div><div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">{filteredPlaces.map((place) => <article key={place.name} className="rounded-2xl border border-slate-100 p-4 transition hover:-translate-y-1 hover:shadow-md"><div className="flex justify-between"><span className="rounded-full bg-orange-50 px-2 py-1 text-xs font-bold text-orange-600">{place.category}</span><span className="text-sm font-bold text-amber-500">★ {place.rating}</span></div><h3 className="mt-4 font-bold">{place.name}</h3><p className="mt-2 text-sm leading-6 text-slate-500">{place.description}</p><div className="mt-4 text-xs font-semibold text-slate-400">{place.estimated_time_hours} hours · {place.entry_fee ? `${place.entry_fee} entry fee` : "Free entry"}</div></article>)}</div></section>}

        {status === "complete" && <section className="mt-6 flex flex-wrap items-center justify-between gap-4 rounded-3xl border border-orange-100 bg-orange-50 p-6"><div><p className="text-xs font-bold uppercase tracking-widest text-orange-500">New feature</p><h2 className="mt-1 text-xl font-bold">Keep this trip for later</h2><p className="mt-1 text-sm text-slate-600">Save your dates in this browser and pick up where you left off.</p></div><button onClick={saveTrip} className="rounded-xl bg-ink px-5 py-3 text-sm font-bold text-white hover:bg-slate-700">♡ Save trip</button></section>}

        {savedTrips.length > 0 && <section className="mt-10"><div className="mb-4 flex items-center justify-between"><h2 className="text-xl font-bold">Saved trips</h2><button onClick={() => setSavedTrips([])} className="text-xs font-bold text-slate-400 hover:text-red-500">Clear all</button></div><div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">{savedTrips.map((trip) => <button onClick={() => loadTrip(trip)} key={trip.id} className="text-left rounded-2xl border border-slate-200 bg-white p-4 transition hover:border-coral"><div className="flex justify-between font-bold"><span>{trip.destination}</span><span className="text-xs text-slate-400">{trip.savedAt}</span></div><div className="mt-2 text-sm text-slate-500">{trip.start_date} → {trip.end_date}</div><div className="mt-3 text-xs font-bold text-coral">Open trip →</div></button>)}</div></section>}
      </main>
    </div>
  );
}

export default App;
