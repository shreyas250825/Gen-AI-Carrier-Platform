import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { User, Target, ArrowLeft } from 'lucide-react';

const LoginPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  // Get the redirect path from location state, default to dashboard
  const from = location.state?.from?.pathname || '/dashboard';
  
  // Check if user is already logged in
  useEffect(() => {
    const savedUser = localStorage.getItem('userEmail');
    if (savedUser) {
      navigate(from, { replace: true });
    }
  }, [navigate, from]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 800));
    
    // Simple demo login - in real app, this would call an API
    if (email && password) {
      localStorage.setItem('userEmail', email);
      
      // Dispatch custom event to notify other components
      window.dispatchEvent(new Event('userLoggedIn'));
      
      navigate(from, { replace: true });
    }
    
    setIsLoading(false);
  };

  const handleGoBack = () => {
    navigate(-1);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950/20 to-slate-950 flex items-center justify-center p-4 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-600/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-sky-600/10 rounded-full blur-3xl animate-pulse delay-1000" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-purple-600/5 rounded-full blur-[120px] animate-pulse delay-500" />
      </div>

      {/* Back Button */}
      <button
        onClick={handleGoBack}
        className="absolute top-8 left-8 z-10 bg-white/10 hover:bg-white/20 backdrop-blur-xl border border-white/20 rounded-full p-3 text-white transition-all group"
      >
        <ArrowLeft className="w-5 h-5 group-hover:-translate-x-1 transition-transform" />
      </button>

      {/* Main Login Container */}
      <div className="w-full max-w-md relative z-10">
        {/* Header */}
        <div className="text-center mb-8">
          {/* Logo */}
          <div className="flex justify-center mb-6">
            <div className="flex h-16 w-16 items-center justify-center rounded-3xl bg-gradient-to-br from-purple-600 to-sky-600 shadow-[0_0_40px_rgba(139,92,246,0.5)] animate-[spin_8s_linear_infinite]">
              <span className="text-lg font-black text-white italic -rotate-12">RS</span>
            </div>
          </div>
          
          <h1 className="text-5xl font-black tracking-tighter uppercase leading-none text-white mb-2">
            WELCOME <span className="text-purple-500 italic">BACK.</span>
          </h1>
          <p className="text-slate-500 text-xs font-bold uppercase tracking-[0.3em]">
            ACCESS YOUR READINESS INTELLIGENCE
          </p>
        </div>

        {/* Login Form */}
        <form onSubmit={handleSubmit} className="p-8 rounded-[32px] border border-white/10 bg-white/5 backdrop-blur-3xl shadow-2xl space-y-6">
          <div className="space-y-4">
            <div className="relative group">
              <User className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-purple-500 transition-colors" size={20} />
              <input
                type="email"
                placeholder="Institutional Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full bg-black/40 border border-white/10 rounded-2xl py-4 pl-12 pr-4 text-white focus:outline-none focus:border-purple-500/50 transition-all placeholder:text-slate-600"
                required
                disabled={isLoading}
              />
            </div>
            
            <div className="relative group">
              <Target className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-purple-500 transition-colors" size={20} />
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-black/40 border border-white/10 rounded-2xl py-4 pl-12 pr-4 text-white focus:outline-none focus:border-purple-500/50 transition-all placeholder:text-slate-600"
                required
                disabled={isLoading}
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-4 bg-purple-600 hover:bg-purple-500 disabled:bg-purple-600/50 text-white font-bold rounded-2xl transition-all shadow-[0_0_30px_rgba(147,51,234,0.3)] hover:shadow-[0_0_40px_rgba(147,51,234,0.5)] disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <div className="flex items-center justify-center gap-2">
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                <span className="text-sm uppercase tracking-[0.2em]">Launching...</span>
              </div>
            ) : (
              <span className="text-sm uppercase tracking-[0.2em]">Launch Studio</span>
            )}
          </button>

          {/* Demo Credentials */}
          <div className="text-center pt-4 border-t border-white/10">
            <p className="text-xs text-slate-500 mb-2 uppercase tracking-wider">Demo Credentials</p>
            <p className="text-xs text-slate-400">Use any email and password to login</p>
          </div>
        </form>

        {/* Footer */}
        <p className="text-center text-xs text-slate-600 uppercase font-black tracking-widest mt-8">
          Secured by ReadySet AI Infrastructure
        </p>
      </div>
    </div>
  );
};

export default LoginPage;