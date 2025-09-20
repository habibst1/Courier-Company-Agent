export const mockShipments = [
  {
    id: 1,
    tracking_number: "TN0001",
    status: "In Transit",
    origin: "New York, NY",
    destination: "Los Angeles, CA",
    expected_delivery: "2024-01-15",
    weight: "2.5 kg"
  },
  {
    id: 2,
    tracking_number: "TN0002",
    status: "Delivered",
    origin: "Chicago, IL",
    destination: "Miami, FL",
    expected_delivery: "2024-01-10",
    weight: "1.2 kg"
  }
];

export const mockTrackingUpdates = [
  {
    id: 1,
    status: "Package Received",
    location: "New York Distribution Center",
    timestamp: "2024-01-10 09:30 AM"
  },
  {
    id: 2,
    status: "In Transit",
    location: "Philadelphia Hub",
    timestamp: "2024-01-11 02:15 PM"
  },
  {
    id: 3,
    status: "Out for Delivery",
    location: "Los Angeles Local Facility",
    timestamp: "2024-01-14 08:45 AM"
  }
];

export const mockUser = {
  id: 1,
  name: "Habib BEN CHEIKH ALI",
  email: "habib.bencheikh@email.com",
  phone: "+216 24123456"
};