import React from 'react';
import { ShoppingCart, Bot, Shield, Sparkles, RefreshCw } from 'lucide-react';

export default function Navbar({
  activeView,
  setActiveView,
  cartCount,
  onOpenCart,
  leadScore,
  leadStatus,
  onResetSession,
  sessionId,
  isChatOpen,
  setIsChatOpen
}) {
  const getStatusBadge = (status) => {
    switch (status) {
      case 'Hot':
        return 'bg-rose-500/10 text-rose-600 border-rose-200';
      case 'Warm':
        return 'bg-amber-500/10 text-amber-600 border-amber-200';
      default:
        return 'bg-blue-500/10 text-blue-600 border-blue-200';
    }
  };

  return (
    <header className="sticky top-0 z-40 bg-white/95 backdrop-blur border-b border-slate-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
        {/* Brand & Academic Info */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-500 flex items-center justify-center text-white shadow-md shadow-indigo-100">
            <Bot className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-lg text-slate-900 tracking-tight">AI-Salesman</span>
              <span className="text-xs px-2 py-0.5 rounded-full font-semibold bg-indigo-50 text-indigo-700 border border-indigo-100">
                MVP v2.0
              </span>
            </div>
            <p className="text-xs text-slate-400 font-medium hidden sm:block">
              Code Connect • Academic Mini-Project #15
            </p>
          </div>
        </div>

        {/* Navigation Tabs (Storefront vs Admin CRM) */}
        <div className="flex items-center bg-slate-100 p-1 rounded-xl border border-slate-200">
          <button
            onClick={() => setActiveView('store')}
            className={`px-3 sm:px-4 py-1.5 rounded-lg text-xs sm:text-sm font-semibold transition-all ${
              activeView === 'store'
                ? 'bg-white text-indigo-600 shadow-sm'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            🛍️ Storefront
          </button>
          <button
            onClick={() => setActiveView('admin')}
            className={`px-3 sm:px-4 py-1.5 rounded-lg text-xs sm:text-sm font-semibold transition-all ${
              activeView === 'admin'
                ? 'bg-white text-indigo-600 shadow-sm'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            📊 Admin CRM
          </button>
        </div>

        {/* Right Action Icons: Live Lead Score, Cart, Reset, Chat Toggle */}
        <div className="flex items-center gap-2 sm:gap-3">
          {/* Live Session Lead Score Badge */}
          <div
            title={`Session: ${sessionId} | Score: ${leadScore} (${leadStatus})`}
            className={`hidden md:flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold border ${getStatusBadge(
              leadStatus
            )}`}
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Lead: {leadScore} pts</span>
            <span className="font-bold uppercase tracking-wider text-[10px]">
              {leadStatus}
            </span>
          </div>

          {/* Reset Session button for testing evaluator workflow */}
          <button
            onClick={onResetSession}
            title="Start Fresh Test Session (Clears current session score and cart)"
            className="p-2 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
          </button>

          {/* Cart Button */}
          <button
            onClick={onOpenCart}
            className="relative p-2 rounded-xl bg-slate-50 hover:bg-slate-100 text-slate-700 border border-slate-200 transition-all flex items-center justify-center"
          >
            <ShoppingCart className="w-5 h-5 text-slate-700" />
            {cartCount > 0 && (
              <span className="absolute -top-1 -right-1 bg-indigo-600 text-white text-[11px] font-bold w-5 h-5 rounded-full flex items-center justify-center animate-pulse">
                {cartCount}
              </span>
            )}
          </button>

          {/* Assistant Chat Toggle */}
          <button
            onClick={() => setIsChatOpen(!isChatOpen)}
            className={`px-3 py-2 rounded-xl text-xs sm:text-sm font-semibold flex items-center gap-1.5 shadow-sm transition-all ${
              isChatOpen
                ? 'bg-indigo-50 text-indigo-600 border border-indigo-200'
                : 'bg-indigo-600 hover:bg-indigo-700 text-white'
            }`}
          >
            <Bot className="w-4 h-4" />
            <span className="hidden sm:inline">AI Assistant</span>
          </button>
        </div>
      </div>
    </header>
  );
}
