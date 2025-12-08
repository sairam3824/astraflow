'use client';

import { useState, useEffect } from 'react';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';

interface Task {
  id: string;
  title: string;
  priority: 'high' | 'low' | 'medium';
  dueDate: string;
  status: 'todo' | 'upcoming';
}

interface Project {
  id: string;
  name: string;
  icon: string;
  color: string;
  tasks: number;
  members: number;
}

interface Goal {
  id: string;
  title: string;
  project: string;
  progress: number;
  color: string;
}

interface CalendarEvent {
  id: string;
  title: string;
  time: string;
  type: string;
  attendees: number;
}

export default function Dashboard() {
  const [currentDate] = useState(new Date());
  const [userName] = useState('User');
  
  const [tasks, setTasks] = useState<Task[]>([
    { id: '1', title: 'One-on-One Meeting', priority: 'high', dueDate: 'Today', status: 'todo' },
    { id: '2', title: 'Send a summary email to stakeholders', priority: 'low', dueDate: '3 days left', status: 'todo' }
  ]);

  const [projects, setProjects] = useState<Project[]>([
    { id: '1', name: 'Product launch', icon: '🚀', color: 'bg-gray-100', tasks: 4, members: 7 },
    { id: '2', name: 'Team brainstorm', icon: '💡', color: 'bg-blue-100', tasks: 4, members: 37 },
    { id: '3', name: 'Branding launch', icon: '💎', color: 'bg-cyan-100', tasks: 3, members: 6 }
  ]);

  const [goals, setGoals] = useState<Goal[]>([
    { id: '1', title: 'Check Emails and Messages', project: 'Product launch • Me Projects', progress: 73, color: 'bg-teal-500' },
    { id: '2', title: 'Prepare a brief status update to the client', project: 'Product launch • Me Projects', progress: 11, color: 'bg-yellow-500' },
    { id: '3', title: 'Update project documentation', project: 'Team brainstorm • Me Projects', progress: 63, color: 'bg-teal-500' }
  ]);

  const [calendarEvents, setCalendarEvents] = useState<CalendarEvent[]>([
    { id: '1', title: 'Meeting with I/P', time: '10:00 - 2:00 am', type: 'Google Meet', attendees: 5 }
  ]);

  const [reminders, setReminders] = useState<string[]>([
    'Assess any new risks identified in the morning meeting',
    'Outline key points by those insight stand on another'
  ]);

  const formatDate = () => {
    return currentDate.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' });
  };

  const getWeekDays = () => {
    const days = [];
    const today = currentDate.getDate();
    const currentDay = currentDate.getDay();
    
    for (let i = 0; i < 7; i++) {
      const date = new Date(currentDate);
      date.setDate(today - currentDay + i);
      days.push({
        day: date.toLocaleDateString('en-US', { weekday: 'short' }),
        date: date.getDate(),
        isToday: i === currentDay
      });
    }
    return days;
  };

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        
        <main className="flex-1 overflow-y-auto">
          <div className="p-8 max-w-7xl mx-auto">
            {/* Welcome Section */}
            <div className="mb-8">
              <div className="text-sm text-gray-500 mb-2">{formatDate()}</div>
              <h1 className="text-3xl font-bold text-gray-900 mb-3">Hello, {userName}</h1>
              <p className="text-xl text-gray-400 mb-4">How can I help you today?</p>
              
              <div className="flex flex-wrap gap-3">
                <button className="px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg text-sm font-medium transition-colors">
                  + Add AI
                </button>
                <button className="px-4 py-2 bg-white hover:bg-gray-50 border border-gray-200 text-gray-700 rounded-lg text-sm font-medium transition-colors">
                  Get tasks updates
                </button>
                <button className="px-4 py-2 bg-white hover:bg-gray-50 border border-gray-200 text-gray-700 rounded-lg text-sm font-medium transition-colors">
                  Create workspace
                </button>
                <button className="px-4 py-2 bg-white hover:bg-gray-50 border border-gray-200 text-gray-700 rounded-lg text-sm font-medium transition-colors">
                  Connect apps
                </button>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Left Column - Tasks and Goals */}
              <div className="lg:col-span-2 space-y-6">
                {/* My Tasks */}
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-2">
                      <span className="text-lg">📋</span>
                      <h2 className="text-lg font-semibold text-gray-900">My Tasks</h2>
                      <button className="text-gray-400 hover:text-gray-600">
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16m-7 6h7" />
                        </svg>
                      </button>
                    </div>
                    <div className="flex items-center space-x-2">
                      <button className="p-1 hover:bg-gray-100 rounded">
                        <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                        </svg>
                      </button>
                      <button className="p-1 hover:bg-gray-100 rounded">
                        <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
                        </svg>
                      </button>
                      <button className="p-1 hover:bg-gray-100 rounded">
                        <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
                        </svg>
                      </button>
                    </div>
                  </div>

                  {/* HUMCOIKERS Section */}
                  <div className="mb-4">
                    <div className="flex items-center space-x-2 mb-3">
                      <button className="text-gray-400 hover:text-gray-600">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                        </svg>
                      </button>
                      <span className="px-2 py-1 bg-purple-100 text-purple-700 text-xs font-medium rounded">HUMCOIKERS</span>
                      <span className="text-sm text-gray-500">• 2 tasks</span>
                    </div>

                    <div className="space-y-2 ml-6">
                      {tasks.filter(t => t.status === 'todo').map((task) => (
                        <div key={task.id} className="flex items-center justify-between py-2 hover:bg-gray-50 rounded-lg px-2">
                          <div className="flex items-center space-x-3 flex-1">
                            <input type="checkbox" className="w-4 h-4 rounded border-gray-300" />
                            <span className="text-gray-900">{task.title}</span>
                          </div>
                          <div className="flex items-center space-x-3">
                            <span className={`px-2 py-1 text-xs font-medium rounded ${
                              task.priority === 'high' ? 'bg-red-100 text-red-700' : 'bg-gray-100 text-gray-700'
                            }`}>
                              {task.priority}
                            </span>
                            <span className={`text-sm ${
                              task.dueDate === 'Today' ? 'text-red-600' : 'text-gray-600'
                            }`}>
                              {task.dueDate}
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  <button className="text-sm text-gray-500 hover:text-gray-700 ml-6">+ Add task</button>

                  {/* UPCOMING Section */}
                  <div className="mt-6">
                    <div className="flex items-center space-x-2 mb-3">
                      <button className="text-gray-400 hover:text-gray-600">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                        </svg>
                      </button>
                      <span className="px-2 py-1 bg-yellow-100 text-yellow-700 text-xs font-medium rounded">UPCOMING</span>
                      <span className="text-sm text-gray-500">• 1 tasks</span>
                    </div>
                  </div>
                </div>

                {/* My Goals */}
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-2">
                      <span className="text-lg">🎯</span>
                      <h2 className="text-lg font-semibold text-gray-900">My Goals</h2>
                    </div>
                  </div>

                  <div className="space-y-4">
                    {goals.map((goal) => (
                      <div key={goal.id} className="space-y-2">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <h3 className="text-gray-900 font-medium">{goal.title}</h3>
                            <p className="text-sm text-gray-500">{goal.project}</p>
                          </div>
                          <span className="text-sm font-semibold text-gray-900">{goal.progress}%</span>
                        </div>
                        <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                          <div 
                            className={`h-full ${goal.color} rounded-full transition-all`}
                            style={{ width: `${goal.progress}%` }}
                          ></div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Right Column - Projects, Calendar, Reminders */}
              <div className="space-y-6">
                {/* Projects */}
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-lg font-semibold text-gray-900">Projects</h2>
                    <button className="text-sm text-gray-500 hover:text-gray-700">Records ▼</button>
                  </div>

                  <button className="w-full flex items-center space-x-3 p-3 border-2 border-dashed border-gray-200 rounded-lg hover:border-gray-300 hover:bg-gray-50 mb-3 transition-colors">
                    <div className="w-8 h-8 bg-gray-100 rounded flex items-center justify-center text-gray-400">+</div>
                    <span className="text-gray-600 font-medium">Create new project</span>
                  </button>

                  <div className="space-y-3">
                    {projects.map((project) => (
                      <div key={project.id} className="flex items-center justify-between p-3 hover:bg-gray-50 rounded-lg cursor-pointer transition-colors">
                        <div className="flex items-center space-x-3">
                          <div className={`w-10 h-10 ${project.color} rounded flex items-center justify-center text-xl`}>
                            {project.icon}
                          </div>
                          <div>
                            <h3 className="font-medium text-gray-900">{project.name}</h3>
                            <p className="text-xs text-gray-500">{project.tasks} tasks • {project.members} Teammates</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Calendar */}
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-lg font-semibold text-gray-900">Calendar</h2>
                    <button className="text-sm text-gray-500 hover:text-gray-700">July ▼</button>
                  </div>

                  <div className="grid grid-cols-7 gap-2 mb-4">
                    {getWeekDays().map((day, idx) => (
                      <div key={idx} className="text-center">
                        <div className="text-xs text-gray-500 mb-1">{day.day}</div>
                        <div className={`w-8 h-8 mx-auto flex items-center justify-center rounded-lg text-sm ${
                          day.isToday ? 'bg-gray-800 text-white font-semibold' : 'text-gray-700'
                        }`}>
                          {day.date}
                        </div>
                      </div>
                    ))}
                  </div>

                  {calendarEvents.map((event) => (
                    <div key={event.id} className="bg-gray-50 rounded-lg p-4 mb-3">
                      <div className="flex items-start justify-between mb-2">
                        <h3 className="font-medium text-gray-900">{event.title}</h3>
                        <button className="text-gray-400 hover:text-gray-600">⋯</button>
                      </div>
                      <p className="text-sm text-gray-600 mb-2">Today • {event.time}</p>
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          <span className="text-xs text-green-600 bg-green-50 px-2 py-1 rounded flex items-center">
                            <span className="mr-1">📹</span>
                            {event.type}
                          </span>
                        </div>
                        <div className="flex -space-x-2">
                          {[...Array(event.attendees)].map((_, i) => (
                            <div key={i} className="w-6 h-6 bg-gradient-to-br from-purple-400 to-pink-400 rounded-full border-2 border-white"></div>
                          ))}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Reminders */}
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-lg font-semibold text-gray-900">Reminders</h2>
                  </div>

                  <div className="mb-3">
                    <button className="text-sm text-gray-500 hover:text-gray-700">Today • 1</button>
                  </div>

                  <div className="space-y-3">
                    {reminders.map((reminder, idx) => (
                      <div key={idx} className="flex items-start space-x-3 group">
                        <input type="checkbox" className="w-4 h-4 mt-0.5 rounded border-gray-300" />
                        <div className="flex-1 flex items-start justify-between">
                          <p className="text-sm text-gray-700 flex-1">{reminder}</p>
                          <div className="flex items-center space-x-1 opacity-0 group-hover:opacity-100 transition-opacity">
                            <button className="p-1 hover:bg-gray-100 rounded">
                              <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                              </svg>
                            </button>
                            <button className="p-1 hover:bg-gray-100 rounded">
                              <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                              </svg>
                            </button>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Invite Section */}
            <div className="mt-6 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl p-6 text-white">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-semibold mb-1">• prodify</h3>
                  <p className="text-sm text-purple-100">New members will gain access to public stuff! Docs and prints made.</p>
                </div>
                <button className="px-6 py-2 bg-white text-purple-600 rounded-lg font-medium hover:bg-gray-50 transition-colors">
                  + Invite people
                </button>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
