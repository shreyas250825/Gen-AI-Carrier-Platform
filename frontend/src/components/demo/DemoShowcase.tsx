import React, { useState, useEffect } from 'react';
import { Upload, Database, Cloud, BarChart3, CheckCircle, AlertCircle, Zap, Shield } from 'lucide-react';

interface DemoStats {
  success: boolean;
  demo_mode: boolean;
  services: {
    s3_storage: {
      status: string;
      mode: string;
      stats: any;
    };
    mongodb_database: {
      status: string;
      mode: string;
      stats: any;
    };
    ai_engines: {
      status: string;
      ollama_requests: number;
      gemini_requests: number;
    };
  };
  platform_metrics: {
    total_users: number;
    interviews_completed: number;
    job_fit_analyses: number;
    average_score: number;
  };
  aws_integration: {
    s3_bucket: string;
    mongodb_atlas: string;
    cloudwatch: string;
    architecture: string;
  };
}

const DemoShowcase: React.FC = () => {
  const [demoStats, setDemoStats] = useState<DemoStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeDemo, setActiveDemo] = useState<string>('overview');
  const [uploadResult, setUploadResult] = useState<any>(null);
  const [analysisResult, setAnalysisResult] = useState<any>(null);

  useEffect(() => {
    fetchDemoStatus();
  }, []);

  const fetchDemoStatus = async () => {
    try {
      const response = await fetch('/api/v1/demo/status');
      const data = await response.json();
      setDemoStats(data);
    } catch (error) {
      console.error('Failed to fetch demo status:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('candidate_name', 'Demo Candidate');
    formData.append('user_id', 'demo_user_001');

    try {
      const response = await fetch('/api/v1/demo/upload-resume', {
        method: 'POST',
        body: formData,
      });
      const result = await response.json();
      setUploadResult(result);
    } catch (error) {
      console.error('Upload failed:', error);
    }
  };

  const runJobFitAnalysis = async () => {
    try {
      const response = await fetch('/api/v1/demo/job-fit-analysis', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          candidate_name: 'Demo Candidate',
          target_role: 'Senior Software Engineer',
          skills: ['Python', 'JavaScript', 'React', 'AWS', 'Docker']
        }),
      });
      const result = await response.json();
      setAnalysisResult(result);
    } catch (error) {
      console.error('Analysis failed:', error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#020617] flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto mb-4"></div>
          <p className="text-white">Loading AWS ImpactX Demo...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#020617] text-white">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 to-sky-600 p-6">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-4xl font-black tracking-tighter uppercase mb-2">
            AWS ImpactX Challenge Demo
          </h1>
          <p className="text-xl opacity-90">
            GenAI Career Intelligence Platform - Live Integration Showcase
          </p>
        </div>
      </div>

      {/* Navigation */}
      <div className="bg-white/[0.03] backdrop-blur-3xl border-b border-white/10">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex space-x-8">
            {[
              { id: 'overview', label: 'Platform Overview', icon: BarChart3 },
              { id: 's3-demo', label: 'S3 Integration', icon: Cloud },
              { id: 'mongodb-demo', label: 'MongoDB Demo', icon: Database },
              { id: 'architecture', label: 'Architecture', icon: Zap }
            ].map(({ id, label, icon: Icon }) => (
              <button
                key={id}
                onClick={() => setActiveDemo(id)}
                className={`flex items-center space-x-2 py-4 px-2 border-b-2 transition-colors ${
                  activeDemo === id
                    ? 'border-purple-500 text-purple-400'
                    : 'border-transparent text-gray-400 hover:text-white'
                }`}
              >
                <Icon className="w-5 h-5" />
                <span>{label}</span>
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Platform Overview */}
        {activeDemo === 'overview' && demoStats && (
          <div className="space-y-8">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-black tracking-tighter uppercase mb-4">
                Platform Status Dashboard
              </h2>
              <p className="text-gray-400 text-lg">
                Real-time monitoring of AWS services integration
              </p>
            </div>

            {/* Status Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-white/[0.03] backdrop-blur-3xl rounded-[32px] p-6 border border-white/10">
                <div className="flex items-center justify-between mb-4">
                  <Cloud className="w-8 h-8 text-blue-400" />
                  <CheckCircle className="w-6 h-6 text-green-400" />
                </div>
                <h3 className="text-xl font-bold mb-2">S3 Storage</h3>
                <p className="text-gray-400 text-sm mb-2">{demoStats.services.s3_storage.mode}</p>
                <p className="text-2xl font-bold text-green-400">
                  {demoStats.services.s3_storage.stats.total_files || 0} Files
                </p>
              </div>

              <div className="bg-white/[0.03] backdrop-blur-3xl rounded-[32px] p-6 border border-white/10">
                <div className="flex items-center justify-between mb-4">
                  <Database className="w-8 h-8 text-green-400" />
                  <CheckCircle className="w-6 h-6 text-green-400" />
                </div>
                <h3 className="text-xl font-bold mb-2">MongoDB</h3>
                <p className="text-gray-400 text-sm mb-2">{demoStats.services.mongodb_database.mode}</p>
                <p className="text-2xl font-bold text-green-400">
                  {demoStats.services.mongodb_database.stats.total_documents || 0} Docs
                </p>
              </div>

              <div className="bg-white/[0.03] backdrop-blur-3xl rounded-[32px] p-6 border border-white/10">
                <div className="flex items-center justify-between mb-4">
                  <Zap className="w-8 h-8 text-purple-400" />
                  <CheckCircle className="w-6 h-6 text-green-400" />
                </div>
                <h3 className="text-xl font-bold mb-2">AI Engines</h3>
                <p className="text-gray-400 text-sm mb-2">Ollama + Gemini</p>
                <p className="text-2xl font-bold text-purple-400">
                  {demoStats.services.ai_engines.ollama_requests + demoStats.services.ai_engines.gemini_requests} Requests
                </p>
              </div>

              <div className="bg-white/[0.03] backdrop-blur-3xl rounded-[32px] p-6 border border-white/10">
                <div className="flex items-center justify-between mb-4">
                  <BarChart3 className="w-8 h-8 text-sky-400" />
                  <CheckCircle className="w-6 h-6 text-green-400" />
                </div>
                <h3 className="text-xl font-bold mb-2">Platform</h3>
                <p className="text-gray-400 text-sm mb-2">Active Users</p>
                <p className="text-2xl font-bold text-sky-400">
                  {demoStats.platform_metrics.total_users.toLocaleString()}
                </p>
              </div>
            </div>

            {/* Metrics Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div className="bg-white/[0.03] backdrop-blur-3xl rounded-[32px] p-8 border border-white/10">
                <h3 className="text-2xl font-bold mb-6">Platform Metrics</h3>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-400">Interviews Completed</span>
                    <span className="text-2xl font-bold text-green-400">
                      {demoStats.platform_metrics.interviews_completed}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-400">Job Fit Analyses</span>
                    <span className="text-2xl font-bold text-blue-400">
                      {demoStats.platform_metrics.job_fit_analyses}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-400">Average Score</span>
                    <span className="text-2xl font-bold text-purple-400">
                      {demoStats.platform_metrics.average_score}%
                    </span>
                  </div>
                </div>
              </div>

              <div className="bg-white/[0.03] backdrop-blur-3xl rounded-[32px] p-8 border border-white/10">
                <h3 className="text-2xl font-bold mb-6">AWS Integration</h3>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-400">S3 Bucket</span>
                    <span className="text-sm font-mono text-green-400">
                      {demoStats.aws_integration.s3_bucket}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-400">MongoDB Atlas</span>
                    <span className="text-sm text-green-400">
                      {demoStats.aws_integration.mongodb_atlas}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-400">Architecture</span>
                    <span className="text-sm text-blue-400">
                      {demoStats.aws_integration.architecture}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* S3 Demo */}
        {activeDemo === 's3-demo' && (
          <div className="space-y-8">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-black tracking-tighter uppercase mb-4">
                Amazon S3 Integration Demo
              </h2>
              <p className="text-gray-400 text-lg">
                File upload and storage demonstration
              </p>
            </div>

            <div className="bg-white/[0.03] backdrop-blur-3xl rounded-[32px] p-8 border border-white/10">
              <h3 className="text-2xl font-bold mb-6 flex items-center">
                <Upload className="w-6 h-6 mr-3 text-blue-400" />
                Resume Upload Demo
              </h3>
              
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-400 mb-2">
                  Upload Resume (PDF, DOC, DOCX)
                </label>
                <input
                  type="file"
                  accept=".pdf,.doc,.docx"
                  onChange={handleFileUpload}
                  className="block w-full text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-purple-600 file:text-white hover:file:bg-purple-700"
                />
              </div>

              {uploadResult && (
                <div className="bg-green-900/20 border border-green-500/30 rounded-[24px] p-6">
                  <h4 className="text-lg font-bold text-green-400 mb-4 flex items-center">
                    <CheckCircle className="w-5 h-5 mr-2" />
                    Upload Successful!
                  </h4>
                  <div className="space-y-2 text-sm">
                    <p><span className="text-gray-400">File URL:</span> <span className="text-green-400 font-mono">{uploadResult.upload_result?.file_url}</span></p>
                    <p><span className="text-gray-400">File Size:</span> <span className="text-white">{uploadResult.upload_result?.file_size} bytes</span></p>
                    <p><span className="text-gray-400">Upload Time:</span> <span className="text-white">{uploadResult.upload_result?.upload_time}</span></p>
                  </div>
                  
                  <div className="mt-4 pt-4 border-t border-green-500/30">
                    <h5 className="font-bold text-green-400 mb-2">Demo Features Showcased:</h5>
                    <div className="grid grid-cols-2 gap-2 text-sm">
                      {Object.entries(uploadResult.demo_features || {}).map(([key, value]) => (
                        <div key={key} className="flex items-center">
                          <CheckCircle className="w-4 h-4 text-green-400 mr-2" />
                          <span>{value}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* MongoDB Demo */}
        {activeDemo === 'mongodb-demo' && (
          <div className="space-y-8">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-black tracking-tighter uppercase mb-4">
                MongoDB Integration Demo
              </h2>
              <p className="text-gray-400 text-lg">
                Real-time data processing and analytics
              </p>
            </div>

            <div className="bg-white/[0.03] backdrop-blur-3xl rounded-[32px] p-8 border border-white/10">
              <h3 className="text-2xl font-bold mb-6 flex items-center">
                <Database className="w-6 h-6 mr-3 text-green-400" />
                Job Fit Analysis Demo
              </h3>
              
              <button
                onClick={runJobFitAnalysis}
                className="bg-gradient-to-r from-purple-600 to-sky-600 text-white px-8 py-3 rounded-[24px] font-bold hover:shadow-[0_0_20px_rgba(139,92,246,0.5)] transition-all duration-300 mb-6"
              >
                Run AI-Powered Job Fit Analysis
              </button>

              {analysisResult && (
                <div className="bg-blue-900/20 border border-blue-500/30 rounded-[24px] p-6">
                  <h4 className="text-lg font-bold text-blue-400 mb-4 flex items-center">
                    <CheckCircle className="w-5 h-5 mr-2" />
                    Analysis Complete!
                  </h4>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    <div>
                      <h5 className="font-bold text-blue-400 mb-2">Fit Score</h5>
                      <p className="text-3xl font-bold text-white">
                        {analysisResult.analysis_result?.overallFitScore}%
                      </p>
                      <p className="text-sm text-gray-400">
                        {analysisResult.analysis_result?.recommendation}
                      </p>
                    </div>
                    <div>
                      <h5 className="font-bold text-blue-400 mb-2">Confidence</h5>
                      <p className="text-3xl font-bold text-white">
                        {analysisResult.analysis_result?.confidenceScore}%
                      </p>
                      <p className="text-sm text-gray-400">AI Confidence Level</p>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <h5 className="font-bold text-green-400 mb-2">Matched Skills</h5>
                      <div className="flex flex-wrap gap-2">
                        {analysisResult.analysis_result?.matchedSkills?.map((skill: string, index: number) => (
                          <span key={index} className="bg-green-900/30 text-green-400 px-3 py-1 rounded-full text-sm">
                            {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                    <div>
                      <h5 className="font-bold text-orange-400 mb-2">Skills to Develop</h5>
                      <div className="flex flex-wrap gap-2">
                        {analysisResult.analysis_result?.missingSkills?.map((skill: string, index: number) => (
                          <span key={index} className="bg-orange-900/30 text-orange-400 px-3 py-1 rounded-full text-sm">
                            {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>

                  <div className="mt-6 pt-4 border-t border-blue-500/30">
                    <h5 className="font-bold text-blue-400 mb-2">Demo Features Showcased:</h5>
                    <div className="grid grid-cols-2 gap-2 text-sm">
                      {Object.entries(analysisResult.demo_features || {}).map(([key, value]) => (
                        <div key={key} className="flex items-center">
                          <CheckCircle className="w-4 h-4 text-blue-400 mr-2" />
                          <span>{value}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Architecture */}
        {activeDemo === 'architecture' && (
          <div className="space-y-8">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-black tracking-tighter uppercase mb-4">
                Platform Architecture
              </h2>
              <p className="text-gray-400 text-lg">
                AWS-powered, scalable, and cost-effective design
              </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div className="bg-white/[0.03] backdrop-blur-3xl rounded-[32px] p-8 border border-white/10">
                <h3 className="text-2xl font-bold mb-6 flex items-center">
                  <Shield className="w-6 h-6 mr-3 text-purple-400" />
                  Core Services
                </h3>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 bg-white/[0.05] rounded-[16px]">
                    <div className="flex items-center">
                      <Cloud className="w-5 h-5 text-blue-400 mr-3" />
                      <span>Amazon S3</span>
                    </div>
                    <span className="text-green-400 text-sm">✅ Active</span>
                  </div>
                  <div className="flex items-center justify-between p-4 bg-white/[0.05] rounded-[16px]">
                    <div className="flex items-center">
                      <Database className="w-5 h-5 text-green-400 mr-3" />
                      <span>MongoDB Atlas</span>
                    </div>
                    <span className="text-green-400 text-sm">✅ Active</span>
                  </div>
                  <div className="flex items-center justify-between p-4 bg-white/[0.05] rounded-[16px]">
                    <div className="flex items-center">
                      <Zap className="w-5 h-5 text-purple-400 mr-3" />
                      <span>Ollama + Gemini AI</span>
                    </div>
                    <span className="text-green-400 text-sm">✅ Active</span>
                  </div>
                </div>
              </div>

              <div className="bg-white/[0.03] backdrop-blur-3xl rounded-[32px] p-8 border border-white/10">
                <h3 className="text-2xl font-bold mb-6">Key Benefits</h3>
                <div className="space-y-4">
                  <div className="flex items-start">
                    <CheckCircle className="w-5 h-5 text-green-400 mr-3 mt-0.5" />
                    <div>
                      <p className="font-semibold">Cost Effective</p>
                      <p className="text-sm text-gray-400">$92-147/month for production</p>
                    </div>
                  </div>
                  <div className="flex items-start">
                    <CheckCircle className="w-5 h-5 text-green-400 mr-3 mt-0.5" />
                    <div>
                      <p className="font-semibold">Privacy First</p>
                      <p className="text-sm text-gray-400">Local AI processing with Ollama</p>
                    </div>
                  </div>
                  <div className="flex items-start">
                    <CheckCircle className="w-5 h-5 text-green-400 mr-3 mt-0.5" />
                    <div>
                      <p className="font-semibold">Highly Scalable</p>
                      <p className="text-sm text-gray-400">Auto-scaling AWS infrastructure</p>
                    </div>
                  </div>
                  <div className="flex items-start">
                    <CheckCircle className="w-5 h-5 text-green-400 mr-3 mt-0.5" />
                    <div>
                      <p className="font-semibold">Enterprise Ready</p>
                      <p className="text-sm text-gray-400">Production-grade security & monitoring</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default DemoShowcase;