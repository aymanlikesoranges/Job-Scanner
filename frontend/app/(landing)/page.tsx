import { EmailAction } from "@/components/email-action";
import { Jobs } from "@/components/jobs";
import Link from "next/link";
import jobs from "@/jobs.json"

export default async function Home() {
  return (
    <div>
      <div className="hero">
        <div className="hero-content text-center">
          <div className="max-w-md">
            <div>
              <Link href="/blog" className="link link-secondary">
                Take me to the blog
              </Link>
              <h1 className="text-3xl font-bold mt-3">Get Job Alerts Before LinkedIn</h1>
              <div className="mt-2">
                <EmailAction></EmailAction>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="mt-6 mx-auto flex justify-center">
        <Jobs jobs={jobs}></Jobs>
      </div>
    </div>
  );
}
