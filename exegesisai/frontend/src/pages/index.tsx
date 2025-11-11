import { useEffect, useState } from "react";

export default function Home() {
	const [health, setHealth] = useState<string>("...");
	const [devotional, setDevotional] = useState<any>(null);

	useEffect(() => {
		const apiBase = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000/api/v1";
		fetch(apiBase.replace(/\/$/, "").replace(/\/v1$/, "") + "/health")
			.then(r => r.json())
			.then(d => setHealth(d.status || "ok"))
			.catch(() => setHealth("unreachable"));

		fetch(`${apiBase}/devotional/today`)
			.then(r => r.json())
			.then(setDevotional)
			.catch(() => setDevotional(null));
	}, []);

	return (
		<main style={{ padding: 24, fontFamily: "sans-serif" }}>
			<h1>ExegesisAI</h1>
			<p>API health: {health}</p>

			<section style={{ marginTop: 24 }}>
				<h2>Devotional (Today)</h2>
				{devotional ? (
					<div>
						<p><strong>{devotional.reference}</strong></p>
						<p>{devotional.text}</p>
						<p><em>{devotional.reflection}</em></p>
					</div>
				) : (
					<p>Loading...</p>
				)}
			</section>
		</main>
	);
}
*** End Patch

