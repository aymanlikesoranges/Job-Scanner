export const metadata = {
  title: "Home - Simple",
  description: "Page description",
};

export function PricingOption({
  price,
  includes,
  missing,
  recurring = false,
}: {
  price: number;
  includes: string[];
  missing: string[];
  recurring: boolean;
}) {
  const priceSuffix = recurring ? "/month" : "";

  return (
    <div>
      <h2>
        ${price}
        <span>{priceSuffix}</span>
      </h2>
      <ul>
        {includes.map((feature, index) => (
          <li className="bg-orange-50" key={index}>
            {feature}
          </li>
        ))}
        {missing.map((feature, index) => (
          <li className="bg-blue-50" key={index}>
            {feature}
          </li>
        ))}
      </ul>
      <button>Buy Now</button>
    </div>
  );
}
export function Pricing() {
  const features = ["Blog", "Automated SEO", "Feature 3"];
  return (
    <div>
      <PricingOption
        price={0}
        includes={features.slice(0, 1)}
        missing={features.slice(1, 3)}
        recurring={true}
      ></PricingOption>
      <PricingOption
        price={0}
        includes={features.slice(0, 1)}
        missing={features.slice(1, 3)}
        recurring={false}
      ></PricingOption>
    </div>
  );
}

export default async function Home() {
  return (
    <>
      <section id="hero" className="px-5">
        <div className="mx-auto">
          <span>Use Blink</span>
          <h1 className="m-0">BLINK</h1>
          <p className="text-lg mt-0">An opensource Next.js template.</p>
          <div className="flex gap-2">
            <button className="btn btn-primary">Buy Now</button>
            <button className="btn">Try Free Version</button>
          </div>
        </div>
        <img></img>
      </section>
      <section id="features" className="px-5">
        <h2 className="features__title">This is a title!</h2>
        <ul className="features">
          <li className="features__list">
            <h3 className="features__title">Login</h3>
            <p className="features__description">
              Built-in OAuth provider powered by Lucia Auth
            </p>
            <code></code>
          </li>
          <li>
            <h3>Payments</h3>
            <p>
              Configure Stripe payments with server components. Sync pricing
              automatically with UI and backend.
            </p>
          </li>
          <li>
            <h3>Blog</h3>
            <p>Built-in blog auto-generaetd from mdx files</p>
          </li>
          <li>
            <h3>Waitlist</h3>
            <p>Get your first users before writing any code</p>
          </li>
          <li>
            <h3>UI Components</h3>
            <p>Styles powered by Tailwind CSS, components included</p>
          </li>
        </ul>
      </section>
      <Pricing />
    </>
  );
}
