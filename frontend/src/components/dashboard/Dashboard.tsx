import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Layout from '../layout/Layout';
import { 
  Video, Brain, Clock, Target, TrendingUp, Trophy, 
  Calendar, PlayCircle, ArrowRight, History, BarChart3, Users
} from 'lucide-react';

const Dashboard = () => {
  const navigate = useNavigate();
  const [userProfile, setUserProfile] = useState<any>(null);
  const [interviewHistory, setInterviewHistory] = useState<any[]>([]);

  // Load user profile and interview history
  useEffect(() => {
    const profile = localStorage.getItem('interviewProfile');
    if (profile) {
      try {
        setUserProfile(JSON.parse(profile));
      } catch (e) {
        // Failed to parse profile, continue with null
      }
    }

    // Load interview history from both localStorage and API
    const loadHistory = async () => {
      // First load from localStorage
      const history = localStorage.getItem('interviewHistory');
      let localHistory: any[] = [];
      if (history) {
        try {
          localHistory = JSON.parse(history);
        } catch (e) {
          // Failed to parse history, continue with empty array
        }
      }

      // Then try to fetch from API and merge
      try {
        const { interviewApi } = await import('../../services/api');
        const apiResponse = await interviewApi.listReports();
        const apiReports = apiResponse.reports || [];
        
        // Merge API data with localStorage, prioritizing API data
        const merged = apiReports.map((apiReport: any) => {
          const localMatch = localHistory.find((h: any) => h.session_id === apiReport.session_id);
          return {
            ...localMatch,
            ...apiReport,
            date: apiReport.created_at ? new Date(apiReport.created_at).toISOString().split('T')[0] : (localMatch?.date || new Date().toISOString().split('T')[0]),
          };
        });
        
        // Add any localStorage-only entries
        const apiSessionIds = new Set(apiReports.map((r: any) => r.session_id));
        const localOnly = localHistory.filter((h: any) => !apiSessionIds.has(h.session_id));
        
        setInterviewHistory([...merged, ...localOnly]);
      } catch (err) {
        // If API fails, use localStorage only
        setInterviewHistory(localHistory);
      }
    };

    loadHistory();
  }, []);

  // Calculate stats from interview history
  const userStats = (() => {
    if (interviewHistory.length === 0) {
      return {
        totalInterviews: 0,
        averageScore: 0,
        improvementRate: 0,
        hoursSpent: 0
      };
    }

    const totalInterviews = interviewHistory.length;
    const scores = interviewHistory.map((i: any) => i.score || 0).filter((s: number) => s > 0);
    const averageScore = scores.length > 0 
      ? Math.round(scores.reduce((a: number, b: number) => a + b, 0) / scores.length)
      : 0;
    
    // Calculate improvement rate (compare last 5 interviews with previous 5)
    let improvementRate = 0;
    if (scores.length >= 10) {
      const recent = scores.slice(-5);
      const previous = scores.slice(-10, -5);
      const recentAvg = recent.reduce((a: number, b: number) => a + b, 0) / recent.length;
      const previousAvg = previous.reduce((a: number, b: number) => a + b, 0) / previous.length;
      improvementRate = Math.round(((recentAvg - previousAvg) / previousAvg) * 100);
    }

    const hoursSpent = interviewHistory.reduce((total: number, i: any) => {
      const duration = i.duration || '0 min';
      const minutes = parseInt(duration) || 0;
      return total + minutes / 60;
    }, 0);

    return {
      totalInterviews,
      averageScore,
      improvementRate: improvementRate || 15, // fallback
      hoursSpent: Math.round(hoursSpent * 10) / 10
    };
  })();

  // Get recent interviews (last 3) from history
  const recentInterviews = interviewHistory.slice(0, 3).map((interview: any) => ({
    id: interview.session_id || interview.id,
    type: interview.interview_type || interview.type || "Technical Interview",
    role: interview.role || userProfile?.estimated_role || userProfile?.role || "Software Engineer",
    date: interview.date || new Date().toISOString().split('T')[0],
    score: interview.score || interview.overallScore || 0,
    duration: interview.duration || "45 min",
    status: "completed"
  }));

  const handleStartInterview = (interviewType?: string) => {
    if (interviewType) {
      // Store interview type preference
      const profile = userProfile || {};
      profile.interview_type = interviewType.toLowerCase();
      localStorage.setItem('interviewProfile', JSON.stringify(profile));
    }
    navigate('/setup');
  };

  const handleViewReport = (sessionId: string) => {
    navigate(`/report?sessionId=${sessionId}`);
  };

  const userName = userProfile?.name || userProfile?.estimated_role || "User";

  return (
    <Layout>
      <div className="min-h-screen bg-[#020617] text-white overflow-x-hidden">
        {/* Animated Background */}
        <div className="fixed inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-1/4 left-1/4 w-[600px] h-[600px] bg-purple-600/10 blur-[150px] rounded-full animate-pulse"></div>
          <div className="absolute bottom-1/4 right-1/4 w-[600px] h-[600px] bg-emerald-400/10 blur-[150px] rounded-full animate-pulse delay-1000"></div>
        </div>

        {/* Hero Section */}
        <section className="relative pt-32 pb-20 px-6 text-center">
          <div className="max-w-6xl mx-auto">
            <div className="inline-block px-4 py-1.5 rounded-full border border-purple-500/20 bg-purple-500/5 text-purple-400 text-[9px] font-black uppercase tracking-[0.4em] mb-6">
              Ready Score Dashboard · {userName}
            </div>
            
            <h1 className="text-6xl md:text-8xl font-black tracking-tighter leading-[0.8] uppercase text-white mb-6">
              YOUR <br/> 
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-white to-emerald-400">
                PROGRESS.
              </span>
            </h1>
            
            <p className="max-w-2xl mx-auto text-lg text-slate-400 font-medium leading-relaxed mb-10">
              Track your interview readiness, analyze performance patterns, and accelerate your career growth.
            </p>
            
            <button 
              onClick={() => handleStartInterview()}
              className="px-12 py-5 bg-white text-black font-black rounded-2xl hover:scale-105 transition-all shadow-[0_0_50px_rgba(255,255,255,0.3)] uppercase text-[10px] tracking-widest"
            >
              Start New Session
            </button>
          </div>
        </section>

        {/* Stats Section */}
        <section className="max-w-7xl mx-auto px-6 mb-20">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-black uppercase tracking-tighter mb-4">Performance <span className="text-purple-500 italic">Metrics.</span></h2>
            <p className="text-slate-500 text-[10px] font-bold uppercase tracking-[0.3em]">Real-Time Intelligence Dashboard</p>
          </div>
          
          <div className="grid md:grid-cols-4 gap-8">
            {[
              { 
                label: "Sessions", 
                value: userStats.totalInterviews, 
                icon: Video, 
                color: "text-emerald-500",
                desc: "Total Practice Sessions"
              },
              { 
                label: "Ready Score", 
                value: userStats.averageScore > 0 ? `${userStats.averageScore}%` : "0%", 
                icon: Trophy, 
                color: "text-purple-500",
                desc: "Average Performance"
              },
              { 
                label: "Growth Rate", 
                value: `+${userStats.improvementRate}%`, 
                icon: TrendingUp, 
                color: "text-blue-500",
                desc: "Improvement Trajectory"
              },
              { 
                label: "Hours", 
                value: userStats.hoursSpent, 
                icon: Clock, 
                color: "text-orange-500",
                desc: "Practice Time Invested"
              }
            ].map((stat, index) => (
              <div key={index} className="glass-panel p-12 rounded-[48px] hover:border-purple-500/40 transition-all group text-center">
                <div className={`mb-8 group-hover:scale-110 transition-transform ${stat.color}`}>
                  <stat.icon size={48} />
                </div>
                <div className="text-4xl font-black uppercase mb-2 tracking-tighter text-white">
                  {stat.value}
                </div>
                <h3 className="text-sm font-black uppercase mb-2 tracking-widest text-white">{stat.label}</h3>
                <p className="text-xs text-slate-500 leading-relaxed">{stat.desc}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Action Center */}
        <section className="max-w-7xl mx-auto px-6 mb-20">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-black uppercase tracking-tighter mb-4">Action <span className="text-emerald-400 italic">Center.</span></h2>
            <p className="text-slate-500 text-[10px] font-bold uppercase tracking-[0.3em]">Launch Your Next Session</p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              { 
                name: "Technical Interview", 
                desc: "Algorithm challenges and system design deep-dives.", 
                icon: Brain, 
                color: "text-red-500",
                type: "technical"
              },
              { 
                name: "Behavioral Round", 
                desc: "Leadership scenarios and culture-fit assessments.", 
                icon: Users, 
                color: "text-emerald-500",
                type: "behavioral"
              },
              { 
                name: "Aptitude Test", 
                desc: "Cognitive ability and logical reasoning evaluation.", 
                icon: Target, 
                color: "text-purple-500",
                route: "/aptitude"
              },
              { 
                name: "Job Fit Analysis", 
                desc: "Role compatibility and skill gap identification.", 
                icon: BarChart3, 
                color: "text-blue-500",
                route: "/job-fit"
              }
            ].map((action, index) => (
              <button
                key={index}
                onClick={() => action.route ? navigate(action.route) : handleStartInterview(action.type)}
                className="glass-panel p-12 rounded-[48px] hover:border-purple-500/40 transition-all group text-left"
              >
                <div className={`mb-8 group-hover:scale-110 transition-transform ${action.color}`}>
                  <action.icon size={32} />
                </div>
                <h3 className="text-sm font-black uppercase mb-4 tracking-widest text-white">{action.name}</h3>
                <p className="text-xs text-slate-500 leading-relaxed">{action.desc}</p>
              </button>
            ))}
          </div>
        </section>

        {/* Recent Activity */}
        <section className="max-w-7xl mx-auto px-6 mb-20">
          <div className="grid md:grid-cols-2 gap-16 items-start">
            <div className="space-y-8">
              <div>
                <h2 className="text-4xl font-black uppercase tracking-tighter mb-4">
                  RECENT <br/><span className="text-purple-500">ACTIVITY.</span>
                </h2>
                <p className="text-slate-400 text-sm leading-relaxed">
                  Your latest interview sessions and performance insights.
                </p>
              </div>
              
              <div className="space-y-4">
                {recentInterviews.length > 0 ? (
                  recentInterviews.map((interview) => (
                    <button
                      key={interview.id}
                      onClick={() => handleViewReport(interview.id)}
                      className="w-full p-6 border border-white/5 bg-white/5 rounded-3xl hover:border-purple-500/40 transition-all text-left group"
                    >
                      <div className="flex items-center justify-between mb-3">
                        <div>
                          <p className="text-sm font-black uppercase tracking-widest text-white group-hover:text-purple-400 transition-colors">
                            {interview.type}
                          </p>
                          <p className="text-xs text-slate-500">{interview.role}</p>
                        </div>
                        <div className="text-right">
                          <p className="text-2xl font-black text-white">{interview.score || 'N/A'}</p>
                          <p className="text-[10px] uppercase text-slate-500 font-bold tracking-[0.2em]">Score</p>
                        </div>
                      </div>
                      <div className="flex items-center justify-between text-xs text-slate-500">
                        <span className="flex items-center">
                          <Calendar className="w-3 h-3 mr-1" />
                          {interview.date}
                        </span>
                        <span className="flex items-center">
                          <Clock className="w-3 h-3 mr-1" />
                          {interview.duration}
                        </span>
                        <ArrowRight className="w-4 h-4 opacity-0 group-hover:opacity-100 transition-opacity" />
                      </div>
                    </button>
                  ))
                ) : (
                  <div className="p-8 border border-white/5 bg-white/5 rounded-3xl text-center">
                    <History className="w-12 h-12 mx-auto mb-4 text-slate-500 opacity-50" />
                    <p className="text-sm text-slate-400 mb-2">No sessions yet</p>
                    <p className="text-xs text-slate-500">Start your first interview to see activity here</p>
                  </div>
                )}
              </div>
              
              {recentInterviews.length > 0 && (
                <button
                  onClick={() => navigate('/reports')}
                  className="flex items-center gap-2 text-[10px] font-bold uppercase tracking-widest text-purple-400 hover:text-purple-300 transition-colors"
                >
                  <span>View All Sessions</span>
                  <ArrowRight size={12} />
                </button>
              )}
            </div>
            
            <div className="glass-panel p-16 rounded-[60px] border border-white/10 bg-white/[0.02] flex items-center justify-center backdrop-blur-3xl">
              <div className="text-center space-y-6">
                <div className="w-32 h-32 bg-purple-600/20 blur-[80px] animate-pulse mx-auto" />
                <div className="space-y-2">
                  <p className="font-mono text-[10px] text-purple-400 uppercase tracking-[0.5em]">AI Intelligence Active</p>
                  <p className="text-xs text-slate-500 max-w-xs mx-auto leading-relaxed">
                    Continuous performance analysis and personalized recommendations powered by advanced ML algorithms.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Quick Actions */}
        <section className="max-w-7xl mx-auto px-6 py-20 border-t border-white/5">
          <div className="grid md:grid-cols-3 gap-8">
            <button
              onClick={() => navigate('/reports')}
              className="flex items-center gap-4 p-6 rounded-2xl bg-white/5 border border-white/5 hover:border-purple-500/40 transition-all group"
            >
              <BarChart3 className="text-purple-500 group-hover:scale-110 transition-transform" size={24} />
              <div className="text-left">
                <p className="text-[10px] font-black uppercase tracking-widest text-white">Performance Analytics</p>
                <p className="text-xs text-slate-500">Detailed session reports</p>
              </div>
            </button>
            
            <button
              onClick={() => navigate('/setup')}
              className="flex items-center gap-4 p-6 rounded-2xl bg-white/5 border border-white/5 hover:border-emerald-500/40 transition-all group"
            >
              <PlayCircle className="text-emerald-500 group-hover:scale-110 transition-transform" size={24} />
              <div className="text-left">
                <p className="text-[10px] font-black uppercase tracking-widest text-white">Quick Start</p>
                <p className="text-xs text-slate-500">Launch new session</p>
              </div>
            </button>
            
            <button
              onClick={() => navigate('/job-fit')}
              className="flex items-center gap-4 p-6 rounded-2xl bg-white/5 border border-white/5 hover:border-blue-500/40 transition-all group"
            >
              <Target className="text-blue-500 group-hover:scale-110 transition-transform" size={24} />
              <div className="text-left">
                <p className="text-[10px] font-black uppercase tracking-widest text-white">Job Matching</p>
                <p className="text-xs text-slate-500">Find your fit</p>
              </div>
            </button>
          </div>
        </section>
      </div>
    </Layout>
  );
};

export default Dashboard;