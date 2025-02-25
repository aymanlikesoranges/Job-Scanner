"use client";
import Link from "next/link";

export default function DefaultLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="prose m-auto mt-5 pb-5">
      <Link className="link link-primary" href="/blog">
        Go back to Blog
      </Link>
      {children}
    </div>
  );
}
