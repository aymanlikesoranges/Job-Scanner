"use client";

import { subscribeWaitlist } from "@/lib/actions";
import { useActionState } from "react";

export function EmailAction({title, description}: { title?: string; description?: string }) {
  const [formState, formAction, isPending] = useActionState(
    subscribeWaitlist,
    null
  );

  return (
    <div>
      <div>
        <span>{description}</span>
        <form action={formAction}>
          <input
            name="email"
            required
            type="email"
            className="input validator input-bordered w-full my-5"
            placeholder="Enter your email"
          />
          <button type="submit" className="btn btn-primary w-full">
            {isPending && (
              <span className="loading loading-spinner loading-sm"></span>
            )}
            {!isPending && "Get notifications for free"}
          </button>
          {formState?.success === false && (
            <div className="error mt-4">{formState.message}</div>
          )}
          {formState?.success === true && (
            <div className="success mt-4">{formState.message}</div>
          )}
        </form>
      </div>
    </div>
  );
}
