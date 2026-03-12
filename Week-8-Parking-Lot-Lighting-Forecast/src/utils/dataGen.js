export const generateParkingData = () => {
  const data = [];
  // Generate 24 hours of data
  for (let i = 0; i < 24; i++) {
    // Vehicle count peaks at 9 AM and 6 PM
    const vehicleCount = Math.floor(
      50 + 200 * Math.exp(-Math.pow(i - 9, 2) / 10) + 
      180 * Math.exp(-Math.pow(i - 18, 2) / 8) + 
      Math.random() * 30
    );
    
    // Lighting usage follows vehicle count but with some non-linearity
    // Light usage % = a + b*count + c*count^2 (simplified)
    const baseUsage = Math.min(100, (vehicleCount / 300) * 100 + (Math.random() * 10));
    
    data.push({
      hour: i,
      vehicles: vehicleCount,
      lighting: Math.round(baseUsage)
    });
  }
  return data;
};
