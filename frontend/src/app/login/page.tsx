"use client";

import { signIn } from "next-auth/react";

export default function LoginPage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100 px-4">
      <div className="w-full max-w-md rounded-2xl bg-white p-8 shadow-md">
        <h1 className="text-center text-3xl font-bold">AI Report Tool</h1>

        <p className="mt-3 text-center text-gray-600">
          Generate company reports using AI + Google Sheets
        </p>

        <button
          onClick={() => signIn("google", { callbackUrl: "/dashboard" })}
          className="mt-8 w-full rounded-xl bg-black py-3 text-white hover:bg-gray-800"
        >
          Continue with Google
        </button>
      </div>
    </div>
  );
}
