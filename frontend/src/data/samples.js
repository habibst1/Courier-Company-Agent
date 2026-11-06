// Real shipments from db/seed.sql, so visitors have tracking numbers that work.
export const sampleShipments = [
  {
    trackingNumber: 'TN4255-8215-9617',
    status: 'in_transit',
    origin: 'Tunis, Tunisia',
    destination: 'Lyon, France',
  },
  {
    trackingNumber: 'FR5657-1034-8818',
    status: 'out_for_delivery',
    origin: 'Paris, France',
    destination: 'Munich, Germany',
  },
  {
    trackingNumber: 'TN7295-5795-1821',
    status: 'delivered',
    origin: 'Tunis, Tunisia',
    destination: 'Paris, France',
  },
];

export const statusLabels = {
  processing: 'Processing',
  in_transit: 'In transit',
  out_for_delivery: 'Out for delivery',
  delivered: 'Delivered',
};

export const statusStyles = {
  processing: 'bg-gray-100 text-gray-800',
  in_transit: 'bg-blue-100 text-blue-800',
  out_for_delivery: 'bg-yellow-100 text-yellow-800',
  delivered: 'bg-green-100 text-green-800',
};
