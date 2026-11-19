import React, { useState, useEffect, useRef } from 'react';
import { Bot, Send, User, Sparkles, X, Minimize2, Maximize2, ShoppingCart, Scale, Flame, ArrowUpRight } from 'lucide-react';

export default function ChatAssistant({
  isOpen,
  onClose,
  sessionId,
  leadScore,
  leadStatus,
  onAddToCart,
  onSelectForCompare,
  externalPrompt,
  onClearExternalPrompt,
  onScoreUpdated
}) {
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      sender: 'bot',
      message: "👋 Hello! I am your AI-Salesman Virtual Assistant. How can I help you today? You can ask about laptops under a budget, compare products, check prices, or ask about our current deals!",
      intent: 'general/greeting',
      suggested_prompts: [
        "Show laptops under $1000",
        "Compare MacBook Air M2 and Asus ZenBook 14",
        "What deals are active today?",
        "Tell me about iPhone 15 Pro"
      ]
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [scoreToast, setScoreToast] = useState(null);
  const [isExpanded, setIsExpanded] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  // Handle external prompts (e.g. user clicked "Ask AI" on a product card or hero chip)
  useEffect(() => {
    if (externalPrompt && externalPrompt.trim()) {
      handleSendMessage(externalPrompt);
      onClearExternalPrompt();
    }
  }, [externalPrompt]);

  const handleSendMessage = async (textToSend) => {
    const text = (textToSend || inputValue).trim();
    if (!text || isLoading) return;

    // Append user message immediately
    const userMsg = {
      id: Date.now().toString(),
      sender: 'customer',
      message: text,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    setMessages(prev => [...prev, userMsg]);
    setInputValue('');
    setIsLoading(true);

    try {
      const res = await fetch('http://127.0.0.1:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          message: text
        })
      });

      if (!res.ok) throw new Error('Failed to get bot response');
      const data = await res.json();

      // Check for score increment toast
      if (data.score_increment > 0) {
        setScoreToast({
          inc: data.score_increment,
          reason: data.scored_reason || 'Action Scored',
          score: data.lead_score,
          status: data.lead_status
        });
        setTimeout(() => setScoreToast(null), 4000);
      }

      if (onScoreUpdated) {
        onScoreUpdated(data.lead_score, data.lead_status);
      }

      const botMsg = {
        id: (Date.now() + 1).toString(),
        sender: 'bot',
        message: data.reply,
        intent: data.intent,
        products: data.products,
        comparison: data.comparison,
        suggested_prompts: data.suggested_prompts,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, botMsg]);
    } catch (err) {
      setMessages(prev => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          sender: 'bot',
          message: "I apologize, but I encountered a momentary connection issue. Please try again or rephrase your question.",
          intent: 'unknown',
          suggested_prompts: ["Show laptops under $1000", "Top electronics", "What deals are active?"]
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div
      className={`fixed bottom-4 right-4 z-50 flex flex-col bg-white border border-slate-200 rounded-3xl shadow-2xl transition-all overflow-hidden ${
        isExpanded ? 'w-[95vw] sm:w-[650px] h-[85vh]' : 'w-[95vw] sm:w-[440px] h-[600px]'
      }`}
    >
      {/* Header */}
      <div className="p-4 bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white flex items-center justify-between shadow-md">
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center text-white shadow-sm">
              <Bot className="w-5 h-5" />
            </div>
            <span className="absolute -bottom-0.5 -right-0.5 w-3 h-3 rounded-full bg-emerald-500 border-2 border-slate-900"></span>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="font-bold text-sm text-white">AI Salesman Assistant</h3>
              <span className="text-[10px] bg-indigo-500/30 text-indigo-200 px-2 py-0.5 rounded-full border border-indigo-400/30">
                Online
              </span>
            </div>
            <div className="flex items-center gap-2 mt-0.5">
              <span className="text-[11px] text-slate-300 font-medium">
                Lead Score: <strong className="text-white">{leadScore} pts</strong>
              </span>
              <span
                className={`text-[9px] font-bold px-1.5 py-0.2 rounded uppercase ${
                  leadStatus === 'Hot'
                    ? 'bg-rose-500 text-white'
                    : leadStatus === 'Warm'
                    ? 'bg-amber-500 text-white'
                    : 'bg-blue-500 text-white'
                }`}
              >
                {leadStatus}
              </span>
            </div>
          </div>
        </div>

        {/* Controls */}
        <div className="flex items-center gap-1">
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="p-1.5 text-slate-300 hover:text-white rounded-lg hover:bg-white/10 transition-colors"
            title={isExpanded ? 'Collapse' : 'Expand'}
          >
            {isExpanded ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
          </button>
          <button
            onClick={onClose}
            className="p-1.5 text-slate-300 hover:text-white rounded-lg hover:bg-white/10 transition-colors"
            title="Close Assistant"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Real-time Lead Scoring Toast Alert */}
      {scoreToast && (
        <div className="bg-amber-500 text-white text-xs px-4 py-2 flex items-center justify-between font-semibold animate-in slide-in-from-top duration-300">
          <div className="flex items-center gap-2">
            <Flame className="w-4 h-4 animate-bounce" />
            <span>
              +{scoreToast.inc} pts ({scoreToast.reason}) • New Score: {scoreToast.score} ({scoreToast.status})
            </span>
          </div>
          <span className="text-[10px] bg-black/20 px-1.5 py-0.5 rounded">FR-LEAD-02</span>
        </div>
      )}

      {/* Messages Stream */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-50/50">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex flex-col ${msg.sender === 'customer' ? 'items-end' : 'items-start'}`}
          >
            <div className="flex items-end gap-2 max-w-[88%]">
              {msg.sender === 'bot' && (
                <div className="w-6 h-6 rounded-lg bg-indigo-600 text-white flex items-center justify-center shrink-0 mb-1 text-xs">
                  <Bot className="w-3.5 h-3.5" />
                </div>
              )}
              <div
                className={`p-3.5 rounded-2xl text-xs sm:text-sm leading-relaxed shadow-xs ${
                  msg.sender === 'customer'
                    ? 'bg-indigo-600 text-white rounded-br-xs'
                    : 'bg-white text-slate-800 border border-slate-200/80 rounded-bl-xs'
                }`}
              >
                {/* Intent Tag Pill for academic review transparency */}
                {msg.intent && msg.sender === 'bot' && (
                  <div className="mb-2 flex items-center gap-1.5">
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-slate-100 text-slate-500 border border-slate-200 uppercase tracking-wider">
                      Intent: {msg.intent}
                    </span>
                  </div>
                )}

                <div className="whitespace-pre-wrap">{msg.message}</div>

                {/* Embedded Comparison Matrix in Chat */}
                {msg.comparison && (
                  <div className="mt-3 p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs">
                    <div className="font-bold text-slate-700 mb-2 flex items-center gap-1">
                      <Scale className="w-3.5 h-3.5 text-indigo-600" />
                      Side-by-Side Spec Matrix:
                    </div>
                    <div className="grid grid-cols-3 gap-1 font-semibold text-[11px] text-slate-500 pb-1 border-b border-slate-200">
                      <span>Feature</span>
                      <span>{msg.comparison.product_a.name.split(' ')[0]}</span>
                      <span>{msg.comparison.product_b.name.split(' ')[0]}</span>
                    </div>
                    <div className="space-y-1.5 pt-1.5 text-[11px]">
                      <div className="grid grid-cols-3 gap-1">
                        <span className="text-slate-500">Price</span>
                        <span className="font-bold text-indigo-600">${msg.comparison.product_a.price}</span>
                        <span className="font-bold text-indigo-600">${msg.comparison.product_b.price}</span>
                      </div>
                      {msg.comparison.spec_matrix.slice(0, 4).map((m, idx) => (
                        <div key={idx} className="grid grid-cols-3 gap-1">
                          <span className="text-slate-500 truncate">{m.feature}</span>
                          <span className="truncate">{String(m.product_a)}</span>
                          <span className="truncate">{String(m.product_b)}</span>
                        </div>
                      ))}
                    </div>
                    <div className="flex gap-2 mt-3 pt-2 border-t border-slate-200">
                      <button
                        onClick={() => onAddToCart(msg.comparison.product_a)}
                        className="flex-1 py-1 px-2 rounded-lg bg-indigo-600 text-white text-[10px] font-bold"
                      >
                        Add {msg.comparison.product_a.name.split(' ')[0]}
                      </button>
                      <button
                        onClick={() => onAddToCart(msg.comparison.product_b)}
                        className="flex-1 py-1 px-2 rounded-lg bg-indigo-600 text-white text-[10px] font-bold"
                      >
                        Add {msg.comparison.product_b.name.split(' ')[0]}
                      </button>
                    </div>
                  </div>
                )}

                {/* Embedded Product Cards in Chat */}
                {msg.products && msg.products.length > 0 && !msg.comparison && (
                  <div className="mt-3 grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                    {msg.products.map((p) => (
                      <div
                        key={p.id}
                        className="bg-slate-50 p-2.5 rounded-xl border border-slate-200 flex flex-col justify-between"
                      >
                        <div className="flex items-center gap-2 mb-2">
                          <img
                            src={p.image_url || 'https://images.unsplash.com/photo-1526738549149-8e07eca6c147?w=500&auto=format&fit=crop&q=60'}
                            alt={p.name}
                            className="w-10 h-10 rounded-lg object-cover bg-white border border-slate-200 shrink-0"
                          />
                          <div className="min-w-0">
                            <h4 className="font-bold text-slate-800 text-xs truncate">{p.name}</h4>
                            <span className="font-extrabold text-indigo-600 text-xs">${p.price.toFixed(2)}</span>
                          </div>
                        </div>
                        <div className="flex gap-1.5 pt-1 border-t border-slate-200">
                          <button
                            onClick={() => onAddToCart(p)}
                            className="flex-1 py-1 px-2 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white text-[10px] font-bold flex items-center justify-center gap-1"
                          >
                            <ShoppingCart className="w-3 h-3" />
                            <span>Add</span>
                          </button>
                          <button
                            onClick={() => handleSendMessage(`Compare ${p.name}`)}
                            title="Compare this product"
                            className="p-1 rounded-lg border border-slate-200 bg-white text-slate-600 hover:text-indigo-600 text-[10px]"
                          >
                            <Scale className="w-3 h-3" />
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Quick Suggestion Chips */}
            {msg.suggested_prompts && msg.suggested_prompts.length > 0 && (
              <div className="mt-2.5 flex flex-wrap gap-1.5 pl-8">
                {msg.suggested_prompts.map((prompt, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleSendMessage(prompt)}
                    className="text-[11px] font-semibold bg-white hover:bg-indigo-50 text-indigo-700 border border-indigo-200 px-2.5 py-1 rounded-full transition-all shadow-2xs hover:border-indigo-300"
                  >
                    {prompt}
                  </button>
                ))}
              </div>
            )}
          </div>
        ))}

        {isLoading && (
          <div className="flex items-center gap-2 text-slate-400 text-xs pl-8">
            <div className="w-2 h-2 rounded-full bg-indigo-600 animate-ping"></div>
            <span>AI Salesman is typing response...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Bar */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSendMessage();
        }}
        className="p-3 bg-white border-t border-slate-200 flex items-center gap-2"
      >
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask price, specs, budget recommendations, or comparisons..."
          className="flex-1 px-4 py-2.5 text-xs sm:text-sm rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500"
        />
        <button
          type="submit"
          disabled={!inputValue.trim() || isLoading}
          className="p-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold disabled:opacity-40 transition-all shadow-sm"
        >
          <Send className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
}
