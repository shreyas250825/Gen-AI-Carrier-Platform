import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Mic, BarChart3, Home, Menu, X, Target, Brain, User } from 'lucide-react';

const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userEmail, setUserEmail] = useState('');
  
  // Check login status on component mount and listen for changes
  useEffect(() => {
    const checkLoginStatus = () => {
      const savedUser = localStorage.getItem('userEmail');
      if (savedUser) {
        setIsLoggedIn(true);
        setUserEmail(savedUser);
      } else {
        setIsLoggedIn(false);
        setUserEmail('');
      }
    };

    // Check on mount
    checkLoginStatus();

    // Listen for storage changes (when user logs in from another tab)
    window.addEventListener('storage', checkLoginStatus);
    
    // Listen for custom login event
    window.addEventListener('userLoggedIn', checkLoginStatus);

    return () => {
      window.removeEventListener('storage', checkLoginStatus);
      window.removeEventListener('userLoggedIn', checkLoginStatus);
    };
  }, []);
  
  // Set active link based on current path
  const getActiveLink = () => {
    const path = location.pathname;
    if (path === '/') return 'home';
    if (path.startsWith('/setup') || path.startsWith('/interview')) return 'interview';
    if (path.startsWith('/dashboard')) return 'dashboard';
    //if (path.startsWith('/reports') || path.startsWith('/report')) return 'reports';
    if (path.startsWith('/job-fit')) return 'jobfit';
    if (path.startsWith('/aptitude')) return 'aptitude';
    // if (path.startsWith('/demo')) return 'demo';
    // if (path.startsWith('/about')) return 'about';
    return '';
  };

  // Check if current page is interview page
  const isInterviewPage = location.pathname.startsWith('/interview');
  
  const [activeLink, setActiveLink] = useState(getActiveLink());
  
  // Update active link when route changes
  useEffect(() => {
    setActiveLink(getActiveLink());
  }, [location.pathname]);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 40);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const navLinks = [
    { id: 'home', label: 'Home', icon: Home, href: '/' },
    { id: 'interview', label: 'Start Interview', icon: Mic, href: '/setup' },
    { id: 'dashboard', label: 'Dashboard', icon: BarChart3, href: '/dashboard' },
    //{ id: 'reports', label: 'Reports', icon: FileText, href: '/reports' },
    { id: 'aptitude', label: 'Aptitude', icon: Brain, href: '/aptitude' },
    { id: 'jobfit', label: 'Job Fit', icon: Target, href: '/job-fit' }
  ];

  const handleLogin = () => {
    navigate('/login', { state: { from: location } });
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUserEmail('');
    localStorage.removeItem('userEmail');
    
    // Dispatch custom event to notify other components
    window.dispatchEvent(new Event('userLoggedOut'));
  };

  return (
    <>
      {/* Fixed Login Button - Top Right Corner */}
      <div className="fixed top-6 right-6 z-[10000]">
        {isLoggedIn ? (
          <div className="flex items-center gap-3">
            <div className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-full px-4 py-2 flex items-center gap-2">
              <User className="w-4 h-4 text-purple-400" />
              <span className="text-xs text-white font-medium">{userEmail.split('@')[0]}</span>
            </div>
            <button
              onClick={handleLogout}
              className="bg-red-500/20 hover:bg-red-500/30 backdrop-blur-xl border border-red-500/30 rounded-full px-4 py-2 text-xs text-red-300 font-medium transition-all"
            >
              Logout
            </button>
          </div>
        ) : (
          <button
            onClick={handleLogin}
            className="bg-purple-600/20 hover:bg-purple-600/30 backdrop-blur-xl border border-purple-500/30 rounded-full px-6 py-3 flex items-center gap-2 text-white font-medium transition-all shadow-[0_0_20px_rgba(139,92,246,0.3)] hover:shadow-[0_0_30px_rgba(139,92,246,0.5)]"
          >
            <User className="w-4 h-4" />
            <span className="text-sm">Login</span>
          </button>
        )}
      </div>

      {/* Login Modal */}
      {/* Removed - Login is now a separate page */}
      {/* Navbar */}
      <header 
        className={`${isInterviewPage ? 'sticky top-0' : 'fixed left-1/2 -translate-x-1/2'} z-[9999] transition-all duration-700 ease-in-out ${
          isInterviewPage 
            ? "w-full" 
            : scrolled 
              ? "top-4 w-[95%] max-w-7xl" 
              : "top-0 w-full"
        }`}
      >
        <nav className={`flex items-center justify-between px-10 py-5 transition-all duration-500 ${
          isInterviewPage
            ? "bg-slate-950/95 backdrop-blur-3xl border-b border-white/10"
            : scrolled 
              ? "bg-white/5 backdrop-blur-3xl border border-white/10 rounded-[32px] shadow-2xl" 
              : "bg-transparent border-b border-white/5"
        }`}>

          
          {/* LEFT: BOLD BRANDING (Fixed Width to prevent layout shifting) */}
          <div onClick={() => navigate('/')} className="flex items-center gap-4 w-[280px] shrink-0 cursor-pointer group">
            <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-purple-600 to-sky-600 shadow-[0_0_20px_rgba(139,92,246,0.5)] animate-[spin_8s_linear_infinite] group-hover:animate-none transition-all duration-300">
              <span className="text-xs font-black text-white italic -rotate-12">RS</span>
            </div>
            <div className="flex flex-col">
              <span className="text-2xl font-black tracking-tighter uppercase leading-none bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">
                ReadySet AI
              </span>
              <span className="text-[10px] text-purple-400 font-bold uppercase tracking-[0.3em] mt-1">
                Interview Coach
              </span>
            </div>
          </div>

          {/* CENTER: NAV LINKS (Centered using flex-grow) */}
          <div className="hidden lg:flex flex-1 justify-center items-center gap-8">
            {navLinks.map((link) => (
              <button
                key={link.id}
                onClick={() => navigate(link.href)}
                className={`text-[11px] font-black uppercase tracking-[0.2em] transition-all relative py-2 px-4 rounded-xl group ${
                  activeLink === link.id ? "text-purple-400" : "text-slate-400 hover:text-white"
                }`}
              >
                <span className="relative flex items-center gap-2">
                  <link.icon className="w-4 h-4" />
                  <span>{link.label}</span>
                </span>
                {activeLink === link.id && (
                  <span className="absolute -bottom-1 left-1/2 transform -translate-x-1/2 w-full h-[3px] bg-purple-500 shadow-[0_0_20px_#a855f7] rounded-full" />
                )}
                {activeLink !== link.id && (
                  <span className="absolute -bottom-1 left-1/2 transform -translate-x-1/2 w-0 group-hover:w-1/2 h-[3px] bg-purple-500 shadow-[0_0_20px_#a855f7] rounded-full transition-all duration-300" />
                )}
              </button>
            ))}
          </div>

          {/* RIGHT: Mobile Menu Button */}
          <div className="w-[120px] flex justify-end">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="lg:hidden bg-white/10 hover:bg-white/20 text-white px-4 py-3 rounded-2xl text-[11px] font-black uppercase tracking-widest transition-all border border-white/10 shadow-[0_0_20px_rgba(255,255,255,0.05)]"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </nav>
      </header>

      {/* Mobile Menu */}
      <div className={`fixed top-0 left-0 w-full z-[9998] lg:hidden transition-all duration-500 overflow-hidden ${
        mobileMenuOpen ? 'max-h-screen opacity-100' : 'max-h-0 opacity-0'
      }`}>
        <div className="bg-slate-950/95 backdrop-blur-3xl border-b border-white/10 pt-24 px-6 py-8 space-y-4">
          {navLinks.map((link) => (
            <button
              key={link.id}
              onClick={() => {
                setActiveLink(link.id);
                setMobileMenuOpen(false);
                navigate(link.href);
              }}
              className={`w-full flex items-center gap-4 px-6 py-4 rounded-2xl font-black text-sm uppercase tracking-[0.2em] transition-all duration-300 ${
                activeLink === link.id
                  ? 'bg-gradient-to-r from-purple-600/20 to-sky-600/20 text-purple-400 border border-purple-500/30 shadow-[0_0_20px_rgba(139,92,246,0.3)]'
                  : 'text-slate-400 hover:text-white hover:bg-white/5 border border-transparent'
              }`}
            >
              <link.icon className="w-5 h-5" />
              <span>{link.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Spacer to prevent content from going under fixed navbar - only for non-interview pages */}
      {!isInterviewPage && <div className="h-20"></div>}
    </>
  );
};

export default Navbar;