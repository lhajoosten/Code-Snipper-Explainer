import { useEffect, useState } from "react";
import axios from "axios";

const API = import.meta.env.VITE_API_BASE_URL;

interface Ping {
  status: string;
  message: string;
}

interface ExplainResponse {
  explanation: string;
  line_count: number;
  placeholder: boolean;
}

export default function App() {
  const [ping, setPing] = useState<Ping | null>(null);
  const [code, setCode] = useState("print('hello world')");
  const [explainResult, setExplainResult] = useState<ExplainResponse | null>(
    null
  );
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    axios
      .get<Ping>(`${API}/ping`)
      .then((r) => setPing(r.data))
      .catch(() => {});
  }, []);

  async function handleExplain() {
    setLoading(true);
    setExplainResult(null);
    try {
      const { data } = await axios.post<ExplainResponse>(`${API}/v1/explain`, {
        code,
      });
      setExplainResult(data);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div
      style={{
        fontFamily: "system-ui, sans-serif",
        maxWidth: 820,
        margin: "0 auto",
        padding: 24,
      }}
    >
      <h1>AI Code Assistant (Minimal)</h1>
      <section style={{ marginBottom: 24 }}>
        <h3>Backend Ping</h3>
        <pre>{ping ? JSON.stringify(ping, null, 2) : "Loading..."}</pre>
      </section>

      <section style={{ marginBottom: 24 }}>
        <h3>Explain (Placeholder)</h3>
        <textarea
          style={{
            width: "100%",
            minHeight: 120,
            fontFamily: "monospace",
            fontSize: 14,
          }}
          value={code}
          onChange={(e) => setCode(e.target.value)}
        />
        <div style={{ marginTop: 8 }}>
          <button onClick={handleExplain} disabled={loading}>
            {loading ? "Explaining..." : "Explain"}
          </button>
        </div>
        {explainResult && (
          <pre
            style={{
              background: "#111",
              color: "#eee",
              padding: 12,
              marginTop: 12,
            }}
          >
            {JSON.stringify(explainResult, null, 2)}
          </pre>
        )}
      </section>

      <footer style={{ marginTop: 48, fontSize: 12, opacity: 0.6 }}>
        Minimal starter. Expand using Clean Architecture layers next.
      </footer>
    </div>
  );
}
