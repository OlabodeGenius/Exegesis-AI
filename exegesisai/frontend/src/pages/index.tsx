import Head from "next/head";
import { useEffect, useMemo, useState } from "react";

type Devotional = {
	reference: string;
	text: string;
	reflection: string;
	date: string;
};

type StudyPreview = {
	reference: string;
	observation?: {
		keywords: string[];
		clauses: string[];
	};
	application?: {
		prompts: { question: string }[];
	};
};

const apiBase = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000/api/v1";

export default function Home() {
	const [health, setHealth] = useState<"checking" | "ok" | "unreachable">("checking");
	const [devotional, setDevotional] = useState<Devotional | null>(null);
	const [study, setStudy] = useState<StudyPreview | null>(null);
	const [error, setError] = useState<string | null>(null);

	const apiRoot = useMemo(() => apiBase.replace(/\/$/, ""), []);

	useEffect(() => {
		fetch(apiRoot.replace(/\/api\/v1$/, "") + "/health")
			.then((r) => r.json())
			.then((d) => setHealth(d.status === "ok" ? "ok" : "unreachable"))
			.catch(() => setHealth("unreachable"));

		fetch(`${apiRoot}/devotional/today`)
			.then((r) => r.json())
			.then((d) => setDevotional(d))
			.catch(() => setDevotional(null));

		fetch(`${apiRoot}/study/run`, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				reference: "Romans 12:2",
				include: ["observation", "application"],
			}),
		})
			.then((r) => {
				if (!r.ok) {
					throw new Error("Failed to fetch study preview");
				}
				return r.json();
			})
			.then((d) => setStudy(d))
			.catch((err) => setError(err.message));
	}, [apiRoot]);

	return (
		<>
			<Head>
				<title>ExegesisAI</title>
			</Head>
			<main style={{ padding: "3rem 1.5rem", fontFamily: "Inter, system-ui, sans-serif", maxWidth: 960, margin: "0 auto" }}>
				<header style={{ marginBottom: "2rem" }}>
					<h1 style={{ fontSize: "2.5rem", marginBottom: "0.5rem" }}>ExegesisAI</h1>
					<p style={{ color: "#475569" }}>
						Observation → Interpretation → Application, powered by approachable ML scaffolding.
					</p>
					<span
						style={{
							display: "inline-flex",
							alignItems: "center",
							gap: "0.5rem",
							fontSize: "0.95rem",
							marginTop: "0.75rem",
							color: health === "ok" ? "#16a34a" : "#dc2626",
						}}
					>
						<strong style={{ fontWeight: 600 }}>API</strong> {health === "checking" ? "checking…" : health}
					</span>
				</header>

				<section style={{ marginBottom: "2.5rem" }}>
					<h2 style={{ fontSize: "1.5rem" }}>Today&apos;s Devotional</h2>
					{devotional ? (
						<article style={{ background: "#f8fafc", padding: "1.25rem", borderRadius: "0.75rem", marginTop: "1rem" }}>
							<p style={{ margin: 0, fontWeight: 600 }}>{devotional.reference}</p>
							<p style={{ marginTop: "0.75rem", fontSize: "1.05rem" }}>{devotional.text}</p>
							<p style={{ marginTop: "0.75rem", fontStyle: "italic", color: "#475569" }}>{devotional.reflection}</p>
						</article>
					) : (
						<p>Loading devotional…</p>
					)}
				</section>

				<section>
					<h2 style={{ fontSize: "1.5rem" }}>Study Preview</h2>
					{error && <p style={{ color: "#dc2626" }}>{error}</p>}
					{study ? (
						<div style={{ display: "grid", gap: "1.25rem", marginTop: "1rem" }}>
							<div style={{ border: "1px solid #e2e8f0", borderRadius: "0.75rem", padding: "1rem" }}>
								<h3 style={{ marginTop: 0, fontSize: "1.2rem" }}>Observation</h3>
								<p>
									<strong>Keywords:</strong>{" "}
									{study.observation?.keywords?.length ? study.observation.keywords.join(", ") : "––"}
								</p>
								<ul>
									{study.observation?.clauses?.map((clause) => (
										<li key={clause}>{clause}</li>
									)) ?? <li>No clauses generated.</li>}
								</ul>
							</div>
							<div style={{ border: "1px solid #e2e8f0", borderRadius: "0.75rem", padding: "1rem" }}>
								<h3 style={{ marginTop: 0, fontSize: "1.2rem" }}>Application Prompts</h3>
								<ul>
									{study.application?.prompts?.map((prompt) => (
										<li key={prompt.question}>{prompt.question}</li>
									)) ?? <li>No prompts generated.</li>}
								</ul>
							</div>
						</div>
					) : (
						<p>Generating study preview…</p>
					)}
				</section>
			</main>
		</>
	);
}
