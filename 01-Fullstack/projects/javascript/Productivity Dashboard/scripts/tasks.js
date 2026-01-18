export let task = {
    id,
    title,
    description,
    priority,
    status,
    timestamp,
};

export let tasks = [];

tasks[0] = {
  id: 1,
  title: "Sample Task",
  description: "Learn JS",
  priority: "high",
  status: "pending",
  timestamp: "2026-01-17T08:00:00"
};

console.log(tasks[0]);
