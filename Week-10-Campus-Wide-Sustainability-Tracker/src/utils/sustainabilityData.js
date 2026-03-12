export const generateSustainabilityData = () => {
  const sectors = ['Academic', 'Hostels', 'Admin', 'Sports'];
  const metrics = ['Energy', 'Water', 'Waste'];
  
  const data = categories => {
    return Array.from({ length: 12 }, (_, i) => ({
      month: format(new Date(2025, i, 1), 'MMM'),
      ...categories.reduce((acc, cat) => ({
        ...acc,
        [cat]: Math.floor(Math.random() * 1000 + 500)
      }), {})
    }));
  };

  const historicalTrends = Array.from({ length: 24 }, (_, i) => ({
    index: i,
    carbon: 400 - i * 5 + Math.random() * 20, // Downward trend
    energy: 1200 - i * 10 + Math.random() * 50
  }));

  return { sectors, metrics, monthlyData: data(sectors), historicalTrends };
};

const format = (date, pattern) => {
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  return months[date.getMonth()];
};
