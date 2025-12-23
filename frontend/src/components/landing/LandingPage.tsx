import React from "react";
import { useNavigate } from "react-router-dom";
import { Zap, Shield, BarChart3, Users, ChevronDown } from "lucide-react";

const LandingPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="overflow-x-hidden">
      {/* 🎬 SECTION 1: PERFECTLY CENTERED HERO */}
      <section className="h-screen w-full flex flex-col items-center justify-center text-center px-6 relative">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-purple-600/10 blur-[150px] rounded-full -z-10 animate-pulse" />
        
        <div className="max-w-6xl animate-fade-in flex flex-col items-center">
          {/* Visual Spacer */}
          <div className="h-16 md:h-24" /> 

          <div className="inline-block px-4 py-1.5 rounded-full border border-purple-500/20 bg-purple-500/5 text-purple-400 text-[9px] font-black uppercase tracking-[0.4em] mb-6">
            AWS ImpactX Finals · Team 403 Forbidden
          </div>
          
          <h1 className="text-8xl md:text-[10rem] font-black tracking-tighter leading-[0.8] uppercase text-white mb-6">
            OWN YOUR <br/> 
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-white to-emerald-400">
              READINESS.
            </span>
          </h1>
          
          <p className="max-w-2xl text-lg text-slate-400 font-medium leading-relaxed mb-10">
            Democratizing career readiness for Tier-2 and Tier-3 institutions through a sentient AI engine that bridges the industry gap.
          </p>
          
          <button 
            onClick={() => navigate('/setup')}
            className="px-12 py-5 bg-white text-black font-black rounded-2xl hover:scale-105 transition-all shadow-[0_0_50px_rgba(255,255,255,0.3)] uppercase text-[10px] tracking-widest"
          >
            Enter Studio
          </button>
        </div>

        {/* Center-aligned Scroll Cue */}
        <div className="absolute bottom-10 flex flex-col items-center gap-2 opacity-20 animate-bounce pointer-events-none">
          <span className="text-[8px] uppercase font-black tracking-[0.5em] ml-1">Scroll</span>
          <ChevronDown size={14} />
        </div>
      </section>

      {/* 🛡️ SCROLLABLE CONTENT AREA */}
      <div className="space-y-40 pb-10">
        
        {/* SECTION 2: THE PREPARATION GAP */}
        <section className="max-w-7xl mx-auto px-6 grid md:grid-cols-2 gap-20 items-center">
          <div className="space-y-8">
            <h2 className="text-6xl font-black uppercase tracking-tighter italic leading-none text-left">
              THE PREPARATION <br/><span className="text-purple-500">GAP.</span>
            </h2>
            <p className="text-slate-400 text-xl leading-relaxed text-left">
              Students in Tier-2 and Tier-3 colleges face a critical mentorship void. We provide high-fidelity guidance.
            </p>
            <div className="grid grid-cols-2 gap-6">
               <div className="p-8 border border-white/5 bg-white/5 rounded-3xl">
                  <p className="text-4xl font-black text-white">60%</p>
                  <p className="text-[10px] uppercase text-slate-500 font-bold tracking-[0.2em]">Confidence Void</p>
               </div>
               <div className="p-8 border border-white/5 bg-white/5 rounded-3xl">
                  <p className="text-4xl font-black text-white">4.2x</p>
                  <p className="text-[10px] uppercase text-slate-500 font-bold tracking-[0.2em]">Success Rate Lift</p>
               </div>
            </div>
          </div>
          <div className="glass-panel p-16 rounded-[60px] border border-white/10 bg-white/[0.02] flex items-center justify-center backdrop-blur-3xl">
             <div className="text-center space-y-4">
                <div className="w-24 h-24 bg-purple-600/20 blur-[60px] animate-pulse mx-auto" />
                <p className="font-mono text-[10px] text-purple-400 uppercase tracking-[0.5em]">Sentinel Intelligence Active</p>
             </div>
          </div>
        </section>

        {/* SECTION 3: CORE INTELLIGENCE FEATURES */}
        <section className="max-w-7xl mx-auto px-6 space-y-20">
          <div className="text-center space-y-4">
            <h2 className="text-4xl font-black uppercase tracking-tighter">Core <span className="text-purple-500 italic">Intelligence.</span></h2>
            <p className="text-slate-500 text-[10px] font-bold uppercase tracking-[0.3em]">Proprietary Sentiment & Logic Engines</p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <USPBox 
              title="Filler Word Destroyer" 
              desc="HUD-style alerts flag verbal crutches like 'um' and 'uh' in real-time." 
              icon={<Shield className="text-red-500" size={32} />} 
            />
            <USPBox 
              title="Smart Adaptation" 
              desc="AI engine adjusts difficulty based on your proficiency in real-time." 
              icon={<Zap className="text-emerald-500" size={32} />} 
            />
            <USPBox 
              title="Skill Radar Map" 
              desc="Visualizing skill gaps through holographic intelligence dashboards." 
              icon={<BarChart3 className="text-purple-500" size={32} />} 
            />
          </div>
        </section>

        {/* SECTION 4: INSTITUTIONAL VISION */}
        <section className="max-w-7xl mx-auto px-6 py-20 border-t border-white/5 text-left">
          <div className="grid md:grid-cols-2 gap-16 items-center">
            <div className="space-y-6">
              <h2 className="text-5xl font-black uppercase tracking-tighter">
                DEMOCRATIZING <br/><span className="text-emerald-400">CAREER READINESS.</span>
              </h2>
              <p className="text-slate-400 leading-relaxed text-sm">
                Our mission is to bridge the mentorship gap for students in Tier-2 and Tier-3 institutions.
              </p>
              <div className="flex items-center gap-4 p-4 rounded-2xl bg-white/5 border border-white/5">
                  <Users className="text-purple-500" size={20} />
                  <p className="text-[10px] font-bold uppercase tracking-widest">Placement Cell Integration</p>
              </div>
            </div>
            <div className="h-40 glass-panel rounded-[40px] flex items-center justify-center">
               <p className="font-mono text-[10px] text-slate-500 uppercase tracking-widest text-center px-6">
                 Empowering 500+ Institutions
               </p>
            </div>
          </div>
        </section>

      </div>
    </div>
  );
};

interface USPBoxProps {
  title: string;
  desc: string;
  icon: React.ReactNode;
}

function USPBox({ title, desc, icon }: USPBoxProps) {
  return (
    <div className="p-12 glass-panel rounded-[48px] hover:border-purple-500/40 transition-all group text-left">
      <div className="mb-8 group-hover:scale-110 transition-transform">{icon}</div>
      <h3 className="text-sm font-black uppercase mb-4 tracking-widest">{title}</h3>
      <p className="text-xs text-slate-500 leading-relaxed">{desc}</p>
    </div>
  );
}

export default LandingPage;
