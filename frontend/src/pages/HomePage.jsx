import { Link } from 'react-router-dom';
import { sampleShipments, statusLabels, statusStyles } from '../data/samples';

const features = [
  {
    title: 'Secure Tracking',
    text: 'Signed-in customers see their own shipment history, and nobody else’s.',
    icon: 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z',
  },
  {
    title: 'Natural Language',
    text: 'Ask questions in plain English and get instant, accurate responses about your shipments.',
    icon: 'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z',
  },
  {
    title: 'Instant Results',
    text: 'Get real-time updates and tracking information without navigating complex menus.',
    icon: 'M13 10V3L4 14h7v7l9-11h-7z',
  },
];

export default function HomePage() {
  return (
    <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <section className="mb-16 mt-8 text-center">
        <h1 className="mb-6 text-4xl font-extrabold leading-tight text-gray-900 md:text-5xl lg:text-6xl">
          AI-Powered <span className="text-primary-600">Courier Tracking</span>
        </h1>
        <p className="mx-auto mb-10 max-w-3xl text-lg text-gray-600 md:text-xl">
          Track your shipments with natural language queries. Ask questions like “Where is my package?” or
          “Show me recent deliveries.”
        </p>
        <div className="flex flex-col justify-center gap-4 sm:flex-row">
          <Link
            to="/authenticated"
            className="rounded-xl bg-primary-600 px-8 py-4 text-lg font-semibold text-white shadow-lg transition hover:-translate-y-0.5 hover:bg-primary-700 hover:shadow-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
          >
            Customer Service Chat
          </Link>
          <Link
            to="/anonymous"
            className="rounded-xl border-2 border-primary-600 bg-white px-8 py-4 text-lg font-semibold text-primary-600 shadow transition hover:-translate-y-0.5 hover:bg-gray-50 hover:shadow-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
          >
            Anonymous Tracking
          </Link>
        </div>
      </section>

      <section className="mb-16 grid gap-8 md:grid-cols-3">
        {features.map((feature) => (
          <div
            key={feature.title}
            className="rounded-xl border border-gray-200 bg-white p-6 shadow-md transition hover:shadow-lg"
          >
            <div className="mb-5 flex h-14 w-14 items-center justify-center rounded-xl bg-primary-50">
              <svg className="h-7 w-7 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={feature.icon} />
              </svg>
            </div>
            <h3 className="mb-3 text-xl font-bold text-gray-900">{feature.title}</h3>
            <p className="text-gray-600">{feature.text}</p>
          </div>
        ))}
      </section>

      <section className="mb-12 rounded-xl border border-gray-200 bg-white p-6 shadow-md">
        <h2 className="mb-2 text-2xl font-bold text-gray-900">Sample Shipments</h2>
        <p className="mb-6 text-gray-600">Real tracking numbers from the demo data. Pick one to try the tracking chat.</p>
        <ul className="space-y-4">
          {sampleShipments.map((shipment) => (
            <li
              key={shipment.trackingNumber}
              className="flex flex-col justify-between gap-3 rounded-lg border border-gray-200 p-4 shadow-sm transition hover:bg-gray-50 hover:shadow sm:flex-row sm:items-center"
            >
              <div>
                <div className="flex flex-wrap items-center gap-2">
                  <span className="font-mono font-semibold text-gray-900">{shipment.trackingNumber}</span>
                  <span className={`rounded-full px-3 py-1 text-xs font-medium ${statusStyles[shipment.status]}`}>
                    {statusLabels[shipment.status]}
                  </span>
                </div>
                <p className="mt-2 text-sm text-gray-600">
                  {shipment.origin} → {shipment.destination}
                </p>
              </div>
              <Link
                to={`/anonymous?number=${encodeURIComponent(shipment.trackingNumber)}`}
                className="self-start rounded-lg px-4 py-2 text-sm font-medium text-primary-600 transition hover:bg-primary-50 focus:outline-none focus:ring-2 focus:ring-primary-500 sm:self-center"
              >
                Track this package →
              </Link>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
