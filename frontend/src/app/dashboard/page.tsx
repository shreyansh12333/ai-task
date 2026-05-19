"use client";

import { useSession } from "next-auth/react";
import { useState } from "react";

type ReportResponse = {
  success: boolean;
  sheet_url: string;
  pdf_url: string;
};

export default function DashboardPage() {
  const { data: session } = useSession();

  const [company, setCompany] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<ReportResponse | null>(null);

  const generateReport = async () => {
    try {
      setLoading(true);
      setError("");
      setResult(null);

      const res = await fetch("/api/generate-report", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          company_name: company,
          access_token: session?.accessToken,
        }),
      });

      if (!res.ok) {
        throw new Error("Failed to generate report");
      }

      const data = await res.json();

      setResult(data);
    } catch (error) {
      setError("Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 px-4 py-10">
      <div className="mx-auto max-w-2xl rounded-2xl bg-white p-8 shadow-md">
        <h1 className="text-3xl font-bold">Generate Company Report</h1>

        <p className="mt-2 text-gray-600">
          Enter a company name and generate a report.
        </p>

        <div className="mt-8 flex gap-3">
          <input
            type="text"
            placeholder="Enter company name"
            value={company}
            onChange={(e) => setCompany(e.target.value)}
            className="flex-1 rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-black"
          />

          <button
            onClick={generateReport}
            disabled={loading}
            className="rounded-xl bg-black px-6 py-3 text-white transition hover:bg-gray-800 disabled:opacity-50"
          >
            {loading ? "Generating..." : "Generate"}
          </button>
        </div>

        {loading && (
          <div className="mt-6 rounded-xl bg-gray-50 p-4">
            <p className="text-sm text-gray-600">Generating AI report...</p>
          </div>
        )}

        {error && (
          <div className="mt-6 rounded-xl bg-red-100 p-4 text-red-600">
            {error}
          </div>
        )}

        {result && (
          <div className="mt-8 rounded-2xl border border-gray-200 p-6">
            <h2 className="text-xl font-semibold">
              Report Generated Successfully
            </h2>

            <div className="mt-6 flex flex-col gap-4">
              <a
                href={result.sheet_url}
                target="_blank"
                className="rounded-xl bg-black px-5 py-3 text-center text-white hover:bg-gray-900"
              >
                Open Google Sheet
              </a>

              <a
                href={result.pdf_url}
                target="_blank"
                className="rounded-xl border border-black px-5 py-3 text-center hover:bg-gray-100"
              >
                Open PDF
              </a>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
