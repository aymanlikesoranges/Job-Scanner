import "@/styles/global.css";

export const metadata = {
  title: "Job Board For Computer Science Students",
  description: "Job board for software and software engineering roles for computer science students. Focused on quality not quantity.",
  icons: {
    icon: [{ url: 'https://cdn.useblink.dev/favicon.ico' }],
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="scroll-smooth" data-theme="light">
      <body className="w-full min-h-screen flex flex-col bg-base-200">
        <main className="flex-grow p-5">{children}</main>
        <footer className="footer footer-center bg-base-300 text-base-content p-4">
          <aside>
            <p>
              Copyright © {new Date().getFullYear()} - All right reserved by NJM
              Developmenet
            </p>
          </aside>
        </footer>
      </body>
    </html>
  );
}
