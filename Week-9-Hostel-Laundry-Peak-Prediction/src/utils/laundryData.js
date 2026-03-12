import { addHours, format, startOfDay } from 'date-fns';

export const generateLaundryHistory = () => {
  const history = [];
  const start = startOfDay(new Date());
  
  // 7 days of historical data
  for (let i = 0; i < 24 * 7; i++) {
    const time = addHours(start, -i);
    const hour = time.getHours();
    const day = time.getDay();
    
    // Weekend peak vs Weekday peak
    let baseLoad = 10;
    if (day === 0 || day === 6) { // Weekend
      baseLoad = 40;
      if (hour >= 10 && hour <= 16) baseLoad += 40;
    } else { // Weekday
      if (hour >= 18 && hour <= 22) baseLoad += 50;
    }
    
    const usage = Math.max(0, Math.min(100, baseLoad + Math.random() * 20 - 10));
    
    // Categorize for Naive Bayes training
    let category = 'Quiet';
    if (usage > 70) category = 'Busy';
    else if (usage > 30) category = 'Normal';

    history.push({
      timestamp: time.toISOString(),
      hour,
      day,
      usage: Math.round(usage),
      category
    });
  }
  return history.reverse();
};

export const classifyState = (history, hour, day) => {
  // Simple Naive Bayes implementation: P(Category | Hour, Day)
  const categories = ['Busy', 'Normal', 'Quiet'];
  const total = history.length;
  
  const results = categories.map(cat => {
    const pCat = history.filter(h => h.category === cat).length / total;
    const pHourGivenCat = history.filter(h => h.category === cat && h.hour === hour).length / 
                         (history.filter(h => h.category === cat).length || 1);
    const pDayGivenCat = history.filter(h => h.category === cat && h.day === day).length / 
                        (history.filter(h => h.category === cat).length || 1);
    
    return { category: cat, probability: pCat * pHourGivenCat * pDayGivenCat };
  });
  
  return results.sort((a, b) => b.probability - a.probability)[0].category;
};
