import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Upload, FileText, Briefcase, Target, TrendingUp, 
  CheckCircle, AlertCircle, ArrowRight, RefreshCw,
  User, MapPin, Calendar, Award, BookOpen, X, FileCheck
} from 'lucide-react';
import Layout from '../layout/Layout';

interface JobDescription {
  title: string;
  company: string;
  required_skills: string[];
  preferred_skills: string[];
  required_experience_years: number;
  location: string;
  description: string;
}

interface JobFitResult {
  overall_fit_score: number;
  skill_match_percentage: number;
  experience_match_percentage: number;
  missing_required_skills: string[];
  missing_preferred_skills: string[];
  matched_skills: string[];
  role_suitability: string;
  recommendations: string[];
}

interface RoleMatch {
  job_description: JobDescription;
  fit_score: number;
  skill_match: number;
  experience_match: number;
  suitability: string;
  missing_skills: string[];
  recommendations: string[];
}

const JobFitAnalysis: React.FC = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<'analyze' | 'matching'>('analyze');
  const [resumeStatus, setResumeStatus] = useState<'none' | 'uploaded' | 'parsing' | 'parsed'>('none');
  const [selectedJob, setSelectedJob] = useState<JobDescription | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [fitResult, setFitResult] = useState<JobFitResult | null>(null);
  const [roleMatches, setRoleMatches] = useState<RoleMatch[]>([]);
  const [userProfile, setUserProfile] = useState<any>(null);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [parseProgress, setParseProgress] = useState(0);

  // Mock job descriptions
  const sampleJobs: JobDescription[] = [
    {
      title: 'Senior Software Engineer',
      company: 'TechCorp',
      required_skills: ['Python', 'JavaScript', 'React', 'Node.js', 'PostgreSQL'],
      preferred_skills: ['AWS', 'Docker', 'TypeScript', 'GraphQL'],
      required_experience_years: 5,
      location: 'San Francisco, CA',
      description: 'We are looking for a senior software engineer to join our growing team...'
    },
    {
      title: 'Frontend Developer',
      company: 'StartupXYZ',
      required_skills: ['JavaScript', 'React', 'HTML', 'CSS'],
      preferred_skills: ['TypeScript', 'Next.js', 'Tailwind CSS'],
      required_experience_years: 3,
      location: 'Remote',
      description: 'Join our frontend team to build amazing user experiences...'
    },
    {
      title: 'Data Scientist',
      company: 'DataCorp',
      required_skills: ['Python', 'Machine Learning', 'SQL', 'Statistics'],
      preferred_skills: ['TensorFlow', 'PyTorch', 'AWS', 'Spark'],
      required_experience_years: 4,
      location: 'New York, NY',
      description: 'We are seeking a data scientist to drive insights from our data...'
    }
  ];

  // Mock role matching results
  const mockRoleMatches: RoleMatch[] = [
    {
      job_description: sampleJobs[0],
      fit_score: 85,
      skill_match: 80,
      experience_match: 90,
      suitability: 'Excellent fit - highly recommended',
      missing_skills: ['GraphQL'],
      recommendations: ['Consider learning GraphQL', 'Highlight your Python experience']
    },
    {
      job_description: sampleJobs[1],
      fit_score: 92,
      skill_match: 95,
      experience_match: 88,
      suitability: 'Excellent fit - highly recommended',
      missing_skills: [],
      recommendations: ['Perfect match for your skills', 'Emphasize React expertise']
    },
    {
      job_description: sampleJobs[2],
      fit_score: 65,
      skill_match: 60,
      experience_match: 70,
      suitability: 'Moderate fit - requires skill development',
      missing_skills: ['Machine Learning', 'Statistics'],
      recommendations: ['Learn machine learning fundamentals', 'Take statistics courses']
    }
  ];

  // Load user profile on mount
  useEffect(() => {
    const profile = localStorage.getItem('interviewProfile');
    if (profile) {
      try {
        const parsedProfile = JSON.parse(profile);
        setUserProfile(parsedProfile);
        setResumeStatus('parsed');
      } catch (e) {
        // Failed to parse profile, continue with no profile
      }
    }
  }, []);

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      // Validate file type
      const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
      if (!allowedTypes.includes(file.type)) {
        alert('Please upload a PDF or Word document');
        return;
      }

      // Validate file size (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        alert('File size must be less than 5MB');
        return;
      }

      setUploadedFile(file);
      setResumeStatus('uploaded');
      
      // Start parsing simulation
      setTimeout(() => {
        setResumeStatus('parsing');
        setParseProgress(0);
        
        // Simulate parsing progress
        const progressInterval = setInterval(() => {
          setParseProgress(prev => {
            if (prev >= 100) {
              clearInterval(progressInterval);
              // Simulate parsed profile data
              const mockParsedProfile = {
                name: 'John Doe',
                email: 'john.doe@email.com',
                phone: '+1 (555) 123-4567',
                location: 'San Francisco, CA',
                estimated_role: 'Software Engineer',
                experience_level: 'Senior',
                experience_years: 5,
                skills: ['Python', 'JavaScript', 'React', 'Node.js', 'PostgreSQL', 'AWS', 'Docker'],
                education: 'Bachelor of Science in Computer Science',
                summary: 'Experienced software engineer with 5+ years in full-stack development',
                work_experience: [
                  {
                    title: 'Senior Software Engineer',
                    company: 'Tech Solutions Inc.',
                    duration: '2021 - Present',
                    description: 'Led development of scalable web applications using React and Node.js'
                  },
                  {
                    title: 'Software Engineer',
                    company: 'StartupXYZ',
                    duration: '2019 - 2021',
                    description: 'Developed frontend components and REST APIs'
                  }
                ]
              };
              
              setUserProfile(mockParsedProfile);
              localStorage.setItem('interviewProfile', JSON.stringify(mockParsedProfile));
              setResumeStatus('parsed');
              return 100;
            }
            return prev + 10;
          });
        }, 200);
      }, 1000);
    }
  };

  const handleRemoveResume = () => {
    setUploadedFile(null);
    setResumeStatus('none');
    setUserProfile(null);
    setParseProgress(0);
    setFitResult(null);
    // Clear the file input
    const fileInput = document.getElementById('resume-upload') as HTMLInputElement;
    if (fileInput) {
      fileInput.value = '';
    }
  };

  const handleAnalyzeFit = async () => {
    if (!selectedJob || !userProfile) return;

    setIsAnalyzing(true);
    try {
      // In a real app, this would be an API call
      // const response = await fetch('/api/job-fit/analyze', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ resume_data: userProfile, job_description: selectedJob })
      // });
      // const result = await response.json();

      // Mock result for demonstration
      const mockResult: JobFitResult = {
        overall_fit_score: 85,
        skill_match_percentage: 80,
        experience_match_percentage: 90,
        missing_required_skills: ['GraphQL'],
        missing_preferred_skills: ['Docker', 'AWS'],
        matched_skills: ['Python', 'JavaScript', 'React', 'Node.js'],
        role_suitability: 'Excellent fit - highly recommended',
        recommendations: [
          'Consider learning GraphQL to strengthen your backend skills',
          'AWS certification would make you even more competitive',
          'Highlight your React and Node.js experience in your application'
        ]
      };

      setTimeout(() => {
        setFitResult(mockResult);
        setIsAnalyzing(false);
      }, 3000);
    } catch (error) {
      // Failed to analyze job fit
      setIsAnalyzing(false);
    }
  };

  const handleRoleMatching = async () => {
    if (!userProfile) return;

    setIsAnalyzing(true);
    try {
      // Mock API call
      setTimeout(() => {
        setRoleMatches(mockRoleMatches);
        setIsAnalyzing(false);
      }, 2000);
    } catch (error) {
      // Failed to find matching roles
      setIsAnalyzing(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-emerald-400';
    if (score >= 60) return 'text-yellow-400';
    return 'text-red-400';
  };

  return (
    <Layout>
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-sky-950 to-slate-900 text-white">
        <div className="max-w-6xl mx-auto px-6 py-8">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold mb-2">AI Job Fit & Role Matching</h1>
            <p className="text-gray-400">Analyze your fit for specific roles and discover matching opportunities</p>
          </div>

          {/* Tab Navigation */}
          <div className="flex justify-center mb-8">
            <div className="bg-slate-800/30 backdrop-blur-xl border border-white/10 rounded-2xl p-2">
              <button
                onClick={() => setActiveTab('analyze')}
                className={`px-6 py-3 rounded-xl font-semibold transition-all ${
                  activeTab === 'analyze'
                    ? 'bg-gradient-to-r from-sky-500 to-cyan-500 text-white'
                    : 'text-gray-400 hover:text-white'
                }`}
              >
                Job Fit Analysis
              </button>
              <button
                onClick={() => setActiveTab('matching')}
                className={`px-6 py-3 rounded-xl font-semibold transition-all ${
                  activeTab === 'matching'
                    ? 'bg-gradient-to-r from-sky-500 to-cyan-500 text-white'
                    : 'text-gray-400 hover:text-white'
                }`}
              >
                Role Matching
              </button>
            </div>
          </div>

          {activeTab === 'analyze' && (
            <div className="space-y-8">
              {/* Resume Status */}
              <div className="bg-slate-800/30 backdrop-blur-xl border border-white/10 rounded-2xl p-6">
                <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                  <FileText className="w-6 h-6 text-sky-400" />
                  Resume Status
                </h3>
                
                {resumeStatus === 'none' && (
                  <div className="text-center py-8">
                    <Upload className="w-16 h-16 mx-auto mb-4 text-gray-400" />
                    <p className="text-gray-400 mb-4">Upload your resume to get started</p>
                    <p className="text-sm text-gray-500 mb-6">Supported formats: PDF, DOC, DOCX (Max 5MB)</p>
                    <label className="inline-flex items-center gap-2 bg-gradient-to-r from-sky-500 to-cyan-500 hover:from-sky-600 hover:to-cyan-600 px-6 py-3 rounded-xl font-semibold cursor-pointer transition-all">
                      <Upload className="w-5 h-5" />
                      Upload Resume
                      <input
                        id="resume-upload"
                        type="file"
                        accept=".pdf,.doc,.docx"
                        onChange={handleFileUpload}
                        className="hidden"
                      />
                    </label>
                  </div>
                )}

                {resumeStatus === 'uploaded' && (
                  <div className="text-center py-8">
                    <FileCheck className="w-16 h-16 mx-auto mb-4 text-sky-400" />
                    <p className="text-sky-400 mb-2">Resume uploaded successfully!</p>
                    <p className="text-sm text-gray-400 mb-4">{uploadedFile?.name}</p>
                    <p className="text-gray-400">Preparing to parse your resume...</p>
                  </div>
                )}

                {resumeStatus === 'parsing' && (
                  <div className="text-center py-8">
                    <div className="w-16 h-16 border-4 border-sky-400 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                    <p className="text-sky-400 mb-4">Parsing your resume...</p>
                    <div className="max-w-md mx-auto">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm text-gray-400">Progress</span>
                        <span className="text-sm text-sky-300">{parseProgress}%</span>
                      </div>
                      <div className="h-2 bg-slate-700/50 rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-gradient-to-r from-sky-400 to-cyan-500 rounded-full transition-all duration-300"
                          style={{ width: `${parseProgress}%` }}
                        ></div>
                      </div>
                      <p className="text-xs text-gray-500 mt-2">
                        {parseProgress < 30 && "Extracting text from document..."}
                        {parseProgress >= 30 && parseProgress < 60 && "Analyzing skills and experience..."}
                        {parseProgress >= 60 && parseProgress < 90 && "Processing work history..."}
                        {parseProgress >= 90 && "Finalizing profile..."}
                      </p>
                    </div>
                  </div>
                )}

                {resumeStatus === 'parsed' && userProfile && (
                  <div>
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center gap-2">
                        <CheckCircle className="w-5 h-5 text-emerald-400" />
                        <span className="text-emerald-400 font-medium">Resume parsed successfully!</span>
                      </div>
                      <button
                        onClick={handleRemoveResume}
                        className="flex items-center gap-2 text-red-400 hover:text-red-300 text-sm transition-colors"
                      >
                        <X className="w-4 h-4" />
                        Remove
                      </button>
                    </div>
                    
                    {uploadedFile && (
                      <div className="mb-4 p-3 bg-slate-700/30 rounded-lg">
                        <div className="flex items-center gap-2 text-sm text-gray-400">
                          <FileText className="w-4 h-4" />
                          <span>{uploadedFile.name}</span>
                          <span>({(uploadedFile.size / 1024 / 1024).toFixed(2)} MB)</span>
                        </div>
                      </div>
                    )}

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <h4 className="font-semibold mb-3 text-emerald-400">Profile Summary</h4>
                        <div className="space-y-2 text-sm">
                          <div className="flex items-center gap-2">
                            <User className="w-4 h-4 text-gray-400" />
                            <span>{userProfile.name || 'N/A'}</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <MapPin className="w-4 h-4 text-gray-400" />
                            <span>{userProfile.location || 'N/A'}</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <Briefcase className="w-4 h-4 text-gray-400" />
                            <span>{userProfile.estimated_role || userProfile.role || 'Software Engineer'}</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <Calendar className="w-4 h-4 text-gray-400" />
                            <span>{userProfile.experience_years || 3} years experience</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <Award className="w-4 h-4 text-gray-400" />
                            <span>{userProfile.experience_level || 'Mid-Level'}</span>
                          </div>
                        </div>
                      </div>
                      <div>
                        <h4 className="font-semibold mb-3 text-sky-400">Key Skills</h4>
                        <div className="flex flex-wrap gap-2">
                          {(userProfile.skills || ['Python', 'JavaScript', 'React']).slice(0, 8).map((skill: string, index: number) => (
                            <span
                              key={index}
                              className="px-3 py-1 bg-sky-400/10 border border-sky-400/30 rounded-full text-xs text-sky-300"
                            >
                              {skill}
                            </span>
                          ))}
                          {(userProfile.skills || []).length > 8 && (
                            <span className="px-3 py-1 bg-gray-600/30 border border-gray-600/30 rounded-full text-xs text-gray-400">
                              +{(userProfile.skills || []).length - 8} more
                            </span>
                          )}
                        </div>
                        
                        {userProfile.summary && (
                          <div className="mt-4">
                            <h5 className="font-medium text-gray-300 mb-2">Summary</h5>
                            <p className="text-sm text-gray-400 leading-relaxed">{userProfile.summary}</p>
                          </div>
                        )}
                      </div>
                    </div>

                    {userProfile.work_experience && userProfile.work_experience.length > 0 && (
                      <div className="mt-6">
                        <h4 className="font-semibold mb-3 text-purple-400">Work Experience</h4>
                        <div className="space-y-3">
                          {userProfile.work_experience.slice(0, 2).map((exp: any, index: number) => (
                            <div key={index} className="p-3 bg-slate-700/30 rounded-lg">
                              <div className="flex items-start justify-between mb-2">
                                <div>
                                  <h5 className="font-medium text-white">{exp.title}</h5>
                                  <p className="text-sm text-gray-400">{exp.company}</p>
                                </div>
                                <span className="text-xs text-gray-500">{exp.duration}</span>
                              </div>
                              <p className="text-sm text-gray-400">{exp.description}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>

              {/* Job Selection */}
              {resumeStatus === 'parsed' && (
                <div className="bg-slate-800/30 backdrop-blur-xl border border-white/10 rounded-2xl p-6">
                  <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                    <Briefcase className="w-6 h-6 text-sky-400" />
                    Select Job Role
                  </h3>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
                    {sampleJobs.map((job, index) => (
                      <button
                        key={index}
                        onClick={() => setSelectedJob(job)}
                        className={`text-left p-4 rounded-xl border transition-all ${
                          selectedJob?.title === job.title
                            ? 'border-sky-400 bg-sky-400/10'
                            : 'border-white/10 bg-slate-700/30 hover:bg-slate-700/50'
                        }`}
                      >
                        <h4 className="font-semibold mb-1">{job.title}</h4>
                        <p className="text-sm text-gray-400 mb-2">{job.company}</p>
                        <div className="flex items-center gap-2 text-xs text-gray-500">
                          <MapPin className="w-3 h-3" />
                          <span>{job.location}</span>
                        </div>
                      </button>
                    ))}
                  </div>

                  {selectedJob && (
                    <div className="bg-slate-700/30 rounded-xl p-4 mb-6">
                      <h4 className="font-semibold mb-2">{selectedJob.title} at {selectedJob.company}</h4>
                      <p className="text-sm text-gray-400 mb-3">{selectedJob.description}</p>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                        <div>
                          <span className="text-sky-400 font-medium">Required Skills:</span>
                          <div className="flex flex-wrap gap-1 mt-1">
                            {selectedJob.required_skills.map((skill, i) => (
                              <span key={i} className="px-2 py-1 bg-red-400/10 text-red-300 rounded text-xs">
                                {skill}
                              </span>
                            ))}
                          </div>
                        </div>
                        <div>
                          <span className="text-sky-400 font-medium">Preferred Skills:</span>
                          <div className="flex flex-wrap gap-1 mt-1">
                            {selectedJob.preferred_skills.map((skill, i) => (
                              <span key={i} className="px-2 py-1 bg-yellow-400/10 text-yellow-300 rounded text-xs">
                                {skill}
                              </span>
                            ))}
                          </div>
                        </div>
                      </div>
                    </div>
                  )}

                  <button
                    onClick={handleAnalyzeFit}
                    disabled={!selectedJob || isAnalyzing}
                    className={`w-full flex items-center justify-center gap-2 px-6 py-3 rounded-xl font-semibold transition-all ${
                      !selectedJob || isAnalyzing
                        ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                        : 'bg-gradient-to-r from-sky-500 to-cyan-500 hover:from-sky-600 hover:to-cyan-600 text-white'
                    }`}
                  >
                    {isAnalyzing ? (
                      <>
                        <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                        Analyzing Fit...
                      </>
                    ) : (
                      <>
                        <Target className="w-5 h-5" />
                        Analyze Job Fit
                      </>
                    )}
                  </button>
                </div>
              )}

              {/* Fit Results */}
              {fitResult && (
                <div className="bg-slate-800/30 backdrop-blur-xl border border-white/10 rounded-2xl p-6">
                  <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
                    <TrendingUp className="w-6 h-6 text-sky-400" />
                    Job Fit Analysis Results
                  </h3>

                  {/* Score Overview */}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    <div className="text-center">
                      <div className={`text-4xl font-bold mb-2 ${getScoreColor(fitResult.overall_fit_score)}`}>
                        {fitResult.overall_fit_score}%
                      </div>
                      <div className="text-gray-400">Overall Fit</div>
                    </div>
                    <div className="text-center">
                      <div className={`text-4xl font-bold mb-2 ${getScoreColor(fitResult.skill_match_percentage)}`}>
                        {fitResult.skill_match_percentage}%
                      </div>
                      <div className="text-gray-400">Skill Match</div>
                    </div>
                    <div className="text-center">
                      <div className={`text-4xl font-bold mb-2 ${getScoreColor(fitResult.experience_match_percentage)}`}>
                        {fitResult.experience_match_percentage}%
                      </div>
                      <div className="text-gray-400">Experience Match</div>
                    </div>
                  </div>

                  {/* Suitability */}
                  <div className="mb-6 p-4 bg-slate-700/30 rounded-xl">
                    <h4 className="font-semibold mb-2 text-emerald-400">Role Suitability</h4>
                    <p className="text-gray-300">{fitResult.role_suitability}</p>
                  </div>

                  {/* Skills Analysis */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    <div>
                      <h4 className="font-semibold mb-3 text-emerald-400 flex items-center gap-2">
                        <CheckCircle className="w-5 h-5" />
                        Matched Skills
                      </h4>
                      <div className="flex flex-wrap gap-2">
                        {fitResult.matched_skills.map((skill, index) => (
                          <span
                            key={index}
                            className="px-3 py-1 bg-emerald-400/10 border border-emerald-400/30 rounded-full text-xs text-emerald-300"
                          >
                            {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                    <div>
                      <h4 className="font-semibold mb-3 text-red-400 flex items-center gap-2">
                        <AlertCircle className="w-5 h-5" />
                        Missing Skills
                      </h4>
                      <div className="space-y-2">
                        {fitResult.missing_required_skills.length > 0 && (
                          <div>
                            <span className="text-xs text-red-300 font-medium">Required:</span>
                            <div className="flex flex-wrap gap-2 mt-1">
                              {fitResult.missing_required_skills.map((skill, index) => (
                                <span
                                  key={index}
                                  className="px-3 py-1 bg-red-400/10 border border-red-400/30 rounded-full text-xs text-red-300"
                                >
                                  {skill}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}
                        {fitResult.missing_preferred_skills.length > 0 && (
                          <div>
                            <span className="text-xs text-yellow-300 font-medium">Preferred:</span>
                            <div className="flex flex-wrap gap-2 mt-1">
                              {fitResult.missing_preferred_skills.map((skill, index) => (
                                <span
                                  key={index}
                                  className="px-3 py-1 bg-yellow-400/10 border border-yellow-400/30 rounded-full text-xs text-yellow-300"
                                >
                                  {skill}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Recommendations */}
                  <div>
                    <h4 className="font-semibold mb-3 text-sky-400 flex items-center gap-2">
                      <BookOpen className="w-5 h-5" />
                      Recommendations
                    </h4>
                    <div className="space-y-2">
                      {fitResult.recommendations.map((rec, index) => (
                        <div key={index} className="flex items-start gap-2 p-3 bg-slate-700/30 rounded-lg">
                          <ArrowRight className="w-4 h-4 text-sky-400 mt-0.5 flex-shrink-0" />
                          <span className="text-sm text-gray-300">{rec}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === 'matching' && (
            <div className="space-y-8">
              {/* Role Matching Header */}
              <div className="bg-slate-800/30 backdrop-blur-xl border border-white/10 rounded-2xl p-6">
                <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                  <Target className="w-6 h-6 text-sky-400" />
                  Find Matching Roles
                </h3>
                <p className="text-gray-400 mb-6">
                  Discover roles that match your skills and experience level
                </p>
                
                <button
                  onClick={handleRoleMatching}
                  disabled={!userProfile || isAnalyzing}
                  className={`flex items-center gap-2 px-6 py-3 rounded-xl font-semibold transition-all ${
                    !userProfile || isAnalyzing
                      ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                      : 'bg-gradient-to-r from-sky-500 to-cyan-500 hover:from-sky-600 hover:to-cyan-600 text-white'
                  }`}
                >
                  {isAnalyzing ? (
                    <>
                      <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      Finding Matches...
                    </>
                  ) : (
                    <>
                      <RefreshCw className="w-5 h-5" />
                      Find Matching Roles
                    </>
                  )}
                </button>
              </div>

              {/* Role Matches */}
              {roleMatches.length > 0 && (
                <div className="space-y-4">
                  <h3 className="text-xl font-bold">Recommended Roles</h3>
                  {roleMatches.map((match, index) => (
                    <div key={index} className="bg-slate-800/30 backdrop-blur-xl border border-white/10 rounded-2xl p-6">
                      <div className="flex items-start justify-between mb-4">
                        <div>
                          <h4 className="text-lg font-semibold mb-1">{match.job_description.title}</h4>
                          <p className="text-gray-400 mb-2">{match.job_description.company}</p>
                          <div className="flex items-center gap-2 text-sm text-gray-500">
                            <MapPin className="w-4 h-4" />
                            <span>{match.job_description.location}</span>
                          </div>
                        </div>
                        <div className="text-right">
                          <div className={`text-3xl font-bold mb-1 ${getScoreColor(match.fit_score)}`}>
                            {match.fit_score}%
                          </div>
                          <div className="text-sm text-gray-400">Fit Score</div>
                        </div>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                        <div>
                          <span className="text-sm text-gray-400">Skill Match: </span>
                          <span className={`font-semibold ${getScoreColor(match.skill_match)}`}>
                            {match.skill_match}%
                          </span>
                        </div>
                        <div>
                          <span className="text-sm text-gray-400">Experience Match: </span>
                          <span className={`font-semibold ${getScoreColor(match.experience_match)}`}>
                            {match.experience_match}%
                          </span>
                        </div>
                      </div>

                      <div className="mb-4 p-3 bg-slate-700/30 rounded-lg">
                        <span className="text-sm font-medium text-emerald-400">Suitability: </span>
                        <span className="text-sm text-gray-300">{match.suitability}</span>
                      </div>

                      {match.missing_skills.length > 0 && (
                        <div className="mb-4">
                          <span className="text-sm font-medium text-red-400">Skills to develop: </span>
                          <div className="flex flex-wrap gap-2 mt-1">
                            {match.missing_skills.map((skill, i) => (
                              <span key={i} className="px-2 py-1 bg-red-400/10 text-red-300 rounded text-xs">
                                {skill}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}

                      <div>
                        <span className="text-sm font-medium text-sky-400">Recommendations: </span>
                        <div className="mt-2 space-y-1">
                          {match.recommendations.map((rec, i) => (
                            <div key={i} className="flex items-start gap-2">
                              <ArrowRight className="w-3 h-3 text-sky-400 mt-1 flex-shrink-0" />
                              <span className="text-xs text-gray-300">{rec}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Back to Dashboard */}
          <div className="flex justify-center mt-8">
            <button
              onClick={() => navigate('/dashboard')}
              className="flex items-center gap-2 bg-slate-700 hover:bg-slate-600 px-6 py-3 rounded-xl font-semibold transition-colors"
            >
              Back to Dashboard
              <ArrowRight className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default JobFitAnalysis;