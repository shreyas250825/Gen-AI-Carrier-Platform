import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Layout from '../layout/Layout';
import { 
  Video, Brain, Clock, Target, Trophy, 
  Calendar, ArrowRight, History, BarChart3, Users
} from 'lucide-react';

const Dashboard = () => {
  const navigate = useNavigate();
  const [userProfile, setUserProfile] = useState<any>(null);
  const [interviewHistory, setInterviewHistory] = useState<any[]>([]);
  const [jobFitAnalyses, setJobFitAnalyses] = useState<any[]>([]);
  const [aptitudeResults, setAptitudeResults] = useState<any[]>([]);
  const [allActivities, setAllActivities] = useState<any[]>([]);

  // Load comprehensive user data
  useEffect(() => {
    const profile = localStorage.getItem('interviewProfile');
    if (profile) {
      try {
        setUserProfile(JSON.parse(profile));
      } catch (e) {
        // Failed to parse profile, continue with null
      }
    }

    // Load all user data from localStorage and APIs
    const loadAllData = async () => {
      // Load interview history
      const history = localStorage.getItem('interviewHistory');
      let localHistory: any[] = [];
      if (history) {
        try {
          localHistory = JSON.parse(history);
        } catch (e) {
          // Failed to parse history, continue with empty array
        }
      }

      // Load job fit analyses
      const jobFitData = localStorage.getItem('jobFitAnalyses');
      let localJobFit: any[] = [];
      if (jobFitData) {
        try {
          localJobFit = JSON.parse(jobFitData);
        } catch (e) {
          // Failed to parse job fit data
        }
      }

      // Load aptitude results
      const aptitudeData = localStorage.getItem('aptitudeResults');
      let localAptitude: any[] = [];
      if (aptitudeData) {
        try {
          localAptitude = JSON.parse(aptitudeData);
        } catch (e) {
          // Failed to parse aptitude data
        }
      }

      // Try to fetch from API and merge
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
            type: 'interview',
            date: apiReport.created_at ? new Date(apiReport.created_at).toISOString().split('T')[0] : (localMatch?.date || new Date().toISOString().split('T')[0]),
          };
        });
        
        // Add any localStorage-only entries
        const apiSessionIds = new Set(apiReports.map((r: any) => r.session_id));
        const localOnly = localHistory.filter((h: any) => !apiSessionIds.has(h.session_id))
          .map(h => ({ ...h, type: 'interview' }));
        
        const allInterviews = [...merged, ...localOnly];
        setInterviewHistory(allInterviews);

        // Set job fit analyses with type
        const jobFitWithType = localJobFit.map(jf => ({ ...jf, type: 'job-fit' }));
        setJobFitAnalyses(jobFitWithType);

        // Set aptitude results with type
        const aptitudeWithType = localAptitude.map(apt => ({ ...apt, type: 'aptitude' }));
        setAptitudeResults(aptitudeWithType);

        // Combine all activities for unified view
        const combined = [
          ...allInterviews,
          ...jobFitWithType,
          ...aptitudeWithType
        ].sort((a, b) => new Date(b.date || b.created_at || new Date()).getTime() - new Date(a.date || a.created_at || new Date()).getTime());

        setAllActivities(combined);

      } catch (err) {
        // If API fails, use localStorage only
        const interviewsWithType = localHistory.map(h => ({ ...h, type: 'interview' }));
        const jobFitWithType = localJobFit.map(jf => ({ ...jf, type: 'job-fit' }));
        const aptitudeWithType = localAptitude.map(apt => ({ ...apt, type: 'aptitude' }));
        
        setInterviewHistory(interviewsWithType);
        setJobFitAnalyses(jobFitWithType);
        setAptitudeResults(aptitudeWithType);

        const combined = [
          ...interviewsWithType,
          ...jobFitWithType,
          ...aptitudeWithType
        ].sort((a, b) => new Date(b.date || b.created_at || new Date()).getTime() - new Date(a.date || a.created_at || new Date()).getTime());

        setAllActivities(combined);
      }
    };

    loadAllData();
  }, []);

  // Calculate comprehensive stats from all activities
  const userStats = (() => {
    const totalInterviews = interviewHistory.length;
    const totalJobFits = jobFitAnalyses.length;
    const totalAptitude = aptitudeResults.length;
    const totalActivities = totalInterviews + totalJobFits + totalAptitude;

    if (totalActivities === 0) {
      return {
        totalInterviews: 0,
        totalJobFits: 0,
        totalAptitude: 0,
        averageScore: 0,
        improvementRate: 0,
        hoursSpent: 0
      };
    }

    // Calculate average scores across all activities
    const interviewScores = interviewHistory.map((i: any) => i.score || i.overall_score || 0).filter((s: number) => s > 0);
    const jobFitScores = jobFitAnalyses.map((jf: any) => jf.overall_fit_score || jf.overallFitScore || 0).filter((s: number) => s > 0);
    const aptitudeScores = aptitudeResults.map((apt: any) => apt.overall_score || apt.score || 0).filter((s: number) => s > 0);
    
    const allScores = [...interviewScores, ...jobFitScores, ...aptitudeScores];
    const averageScore = allScores.length > 0 
      ? Math.round(allScores.reduce((a: number, b: number) => a + b, 0) / allScores.length)
      : 0;
    
    // Calculate improvement rate (compare recent activities with older ones)
    let improvementRate = 0;
    if (allScores.length >= 6) {
      const recent = allScores.slice(-3);
      const previous = allScores.slice(-6, -3);
      const recentAvg = recent.reduce((a: number, b: number) => a + b, 0) / recent.length;
      const previousAvg = previous.reduce((a: number, b: number) => a + b, 0) / previous.length;
      improvementRate = Math.round(((recentAvg - previousAvg) / previousAvg) * 100);
    }

    const hoursSpent = interviewHistory.reduce((total: number, i: any) => {
      const duration = i.duration || '0 min';
      const minutes = parseInt(duration) || 45; // Default 45 min per interview
      return total + minutes / 60;
    }, 0) + (totalJobFits * 0.5) + (totalAptitude * 0.75); // Estimate time for other activities

    return {
      totalInterviews,
      totalJobFits,
      totalAptitude,
      averageScore,
      improvementRate: improvementRate || 15, // fallback
      hoursSpent: Math.round(hoursSpent * 10) / 10
    };
  })();

  // Get recent activities (limited to 5 for dashboard overview)
  const recentActivities = allActivities.slice(0, 5).map((activity: any) => {
    if (activity.type === 'interview') {
      return {
        id: activity.session_id || activity.id,
        type: "Interview",
        subtype: activity.interview_type || activity.type || "Technical Interview",
        role: activity.role || userProfile?.estimated_role || userProfile?.role || "Software Engineer",
        date: activity.date || new Date().toISOString().split('T')[0],
        score: activity.score || activity.overall_score || 0,
        duration: activity.duration || "45 min",
        status: "completed",
        icon: "🎤",
        color: "text-blue-500"
      };
    } else if (activity.type === 'job-fit') {
      return {
        id: activity.id || `jobfit_${Date.now()}`,
        type: "Job Fit Analysis",
        subtype: activity.targetRole || activity.role || "Software Engineer",
        role: activity.targetRole || activity.role || "Software Engineer",
        date: activity.date || activity.createdAt || new Date().toISOString().split('T')[0],
        score: activity.overall_fit_score || activity.overallFitScore || 0,
        duration: "30 min",
        status: "completed",
        icon: "🎯",
        color: "text-emerald-500"
      };
    } else if (activity.type === 'aptitude') {
      return {
        id: activity.id || `aptitude_${Date.now()}`,
        type: "Aptitude Test",
        subtype: activity.test_type || "Comprehensive Assessment",
        role: "General Assessment",
        date: activity.date || activity.completedAt || new Date().toISOString().split('T')[0],
        score: activity.overall_score || activity.score || 0,
        duration: activity.duration || "45 min",
        status: "completed",
        icon: "🧠",
        color: "text-purple-500"
      };
    }
    return activity;
  });

  const handleStartInterview = (interviewType?: string) => {
    if (interviewType) {
      // Store interview type preference
      const profile = userProfile || {};
      profile.interview_type = interviewType.toLowerCase();
      localStorage.setItem('interviewProfile', JSON.stringify(profile));
    }
    navigate('/setup');
  };

  const handleViewReport = (activityId: string, activityType: string) => {
    if (activityType === 'Interview') {
      navigate(`/report?sessionId=${activityId}`);
    } else if (activityType === 'Job Fit Analysis') {
      navigate(`/job-fit?analysisId=${activityId}`);
    } else if (activityType === 'Aptitude Test') {
      navigate(`/aptitude?resultId=${activityId}`);
    }
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
                label: "Interviews", 
                value: userStats.totalInterviews, 
                icon: Video, 
                color: "text-blue-500",
                desc: "Technical & Behavioral Sessions"
              },
              { 
                label: "Job Fits", 
                value: userStats.totalJobFits, 
                icon: Target, 
                color: "text-emerald-500",
                desc: "Role Compatibility Analyses"
              },
              { 
                label: "Aptitude Tests", 
                value: userStats.totalAptitude, 
                icon: Brain, 
                color: "text-purple-500",
                desc: "Logical & Quantitative Assessments"
              },
              { 
                label: "Avg Score", 
                value: userStats.averageScore > 0 ? `${userStats.averageScore}%` : "0%", 
                icon: Trophy, 
                color: "text-orange-500",
                desc: "Overall Performance Average"
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
                {recentActivities.length > 0 ? (
                  recentActivities.map((activity) => (
                    <button
                      key={activity.id}
                      onClick={() => handleViewReport(activity.id, activity.type)}
                      className="w-full p-6 border border-white/5 bg-white/5 rounded-3xl hover:border-purple-500/40 transition-all text-left group"
                    >
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center gap-3">
                          <span className="text-2xl">{activity.icon}</span>
                          <div>
                            <p className="text-sm font-black uppercase tracking-widest text-white group-hover:text-purple-400 transition-colors">
                              {activity.type}
                            </p>
                            <p className="text-xs text-slate-500">{activity.subtype}</p>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="text-2xl font-black text-white">{activity.score || 'N/A'}</p>
                          <p className="text-[10px] uppercase text-slate-500 font-bold tracking-[0.2em]">Score</p>
                        </div>
                      </div>
                      <div className="flex items-center justify-between text-xs text-slate-500">
                        <span className="flex items-center">
                          <Calendar className="w-3 h-3 mr-1" />
                          {activity.date}
                        </span>
                        <span className="flex items-center">
                          <Clock className="w-3 h-3 mr-1" />
                          {activity.duration}
                        </span>
                        <ArrowRight className="w-4 h-4 opacity-0 group-hover:opacity-100 transition-opacity" />
                      </div>
                    </button>
                  ))
                ) : (
                  <div className="p-8 border border-white/5 bg-white/5 rounded-3xl text-center">
                    <History className="w-12 h-12 mx-auto mb-4 text-slate-500 opacity-50" />
                    <p className="text-sm text-slate-400 mb-2">No activities yet</p>
                    <p className="text-xs text-slate-500">Start your first assessment to see activity here</p>
                  </div>
                )}
              </div>
              
              {recentActivities.length > 0 && (
                <div className="text-center">
                  <button
                    onClick={() => navigate('/reports')}
                    className="inline-flex items-center gap-3 px-6 py-3 bg-gradient-to-r from-purple-600 to-sky-600 hover:from-purple-700 hover:to-sky-700 rounded-xl font-bold transition-all transform hover:scale-105 shadow-[0_0_20px_rgba(139,92,246,0.5)]"
                  >
                    <BarChart3 className="w-4 h-4" />
                    <span>View All Reports</span>
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
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

        {/* View Reports Section */}
        <section className="max-w-7xl mx-auto px-6 py-20 border-t border-white/5">
          <div className="text-center">
            <h2 className="text-4xl font-black uppercase tracking-tighter mb-4">View All <span className="text-emerald-400 italic">Reports.</span></h2>
            <p className="text-slate-500 text-[10px] font-bold uppercase tracking-[0.3em] mb-8">Access Complete Activity History & Analytics</p>
            
            <button
              onClick={() => navigate('/reports')}
              className="relative group"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-emerald-400 to-sky-500 rounded-xl blur opacity-75 group-hover:opacity-100 transition-opacity"></div>
              <div className="relative flex items-center justify-center space-x-3 bg-gradient-to-r from-emerald-500 to-sky-500 px-8 py-4 rounded-xl font-semibold transform group-hover:scale-105 transition-all duration-300">
                <BarChart3 className="w-5 h-5" />
                <span>View All Reports</span>
                <ArrowRight className="w-5 h-5" />
              </div>
            </button>
            
            <p className="text-xs text-slate-500 mt-4 max-w-md mx-auto">
              Access detailed analysis, performance trends, and comprehensive reports for all your interviews, job fits, and aptitude tests.
            </p>
          </div>
        </section>
      </div>
    </Layout>
  );
};

export default Dashboard;