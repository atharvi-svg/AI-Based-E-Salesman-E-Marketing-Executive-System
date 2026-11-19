import React from 'react';
import { Search, Filter, Sparkles, Scale, X } from 'lucide-react';
import ProductCard from './ProductCard';

const CATEGORIES = ['all', 'Laptops', 'Smartphones', 'Audio', 'Smartwatches', 'Tablets', 'Accessories'];
const BUDGET_OPTIONS = [
  { label: 'All Budgets', value: null },
  { label: 'Under $500', value: 500 },
  { label: 'Under $1,000', value: 1000 },
  { label: 'Under $1,500', value: 1500 },
];

export default function ProductCatalog({
  products,
  loading,
  selectedCategory,
  setSelectedCategory,
  selectedBudget,
  setSelectedBudget,
  searchQuery,
  setSearchQuery,
  onAddToCart,
  onAskAI,
  compareItems,
  onSelectForCompare,
  onTriggerCompare,
  onClearCompare
}) {
  return (
    <div className="space-y-6">
      {/* Hero Banner with Quick Assistant Prompt */}
      <div className="relative rounded-3xl overflow-hidden bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white p-6 sm:p-8 shadow-xl">
        <div className="max-w-2xl">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-semibold mb-3 border border-indigo-500/30">
            <Sparkles className="w-3.5 h-3.5" />
            AI-Powered Sales & Marketing System
          </div>
          <h1 className="text-2xl sm:text-4xl font-extrabold tracking-tight mb-2">
            Smart Tech Catalog & Virtual Assistant
          </h1>
          <p className="text-slate-300 text-sm sm:text-base leading-relaxed mb-6">
            Explore 24+ top electronic devices, compare specifications side-by-side, ask our AI assistant for budget recommendations, and complete your instant simulated order.
          </p>
          <div className="flex flex-wrap gap-2 text-xs font-medium">
            <span className="text-slate-400">Try asking the AI:</span>
            <button
              onClick={() => onAskAI({ name: 'Laptops under $1000' })}
              className="px-2.5 py-1 rounded-lg bg-white/10 hover:bg-white/20 text-indigo-200 transition-colors"
            >
              "Laptops under $1000"
            </button>
            <button
              onClick={() => onAskAI({ name: 'Compare MacBook Air M2 and Asus ZenBook 14' })}
              className="px-2.5 py-1 rounded-lg bg-white/10 hover:bg-white/20 text-indigo-200 transition-colors"
            >
              "Compare MacBook Air vs ZenBook"
            </button>
            <button
              onClick={() => onAskAI({ name: 'What deals do you have today?' })}
              className="px-2.5 py-1 rounded-lg bg-white/10 hover:bg-white/20 text-indigo-200 transition-colors"
            >
              "Today's Offers"
            </button>
          </div>
        </div>
      </div>

      {/* Floating Comparison Drawer if products selected */}
      {compareItems.length > 0 && (
        <div className="sticky top-20 z-30 bg-white border border-indigo-200 p-4 rounded-2xl shadow-lg flex items-center justify-between gap-4 animate-in fade-in slide-in-from-top-2">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center font-bold">
              <Scale className="w-4 h-4" />
            </div>
            <div>
              <p className="text-xs font-bold text-slate-800">
                Compare Products ({compareItems.length}/2 selected)
              </p>
              <p className="text-xs text-slate-500">
                {compareItems.map(p => p.name).join(' vs ')}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            {compareItems.length === 2 && (
              <button
                onClick={onTriggerCompare}
                className="px-4 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold shadow-sm transition-all"
              >
                Compare Specs Side-by-Side
              </button>
            )}
            <button
              onClick={onClearCompare}
              className="p-1.5 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-100"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* Controls Bar: Search & Filters */}
      <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm space-y-4">
        {/* Search & Budget Controls */}
        <div className="flex flex-col sm:flex-row gap-3 items-center justify-between">
          <div className="relative w-full sm:w-80">
            <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search by product name, brand, or feature..."
              className="w-full pl-9 pr-4 py-2 text-xs sm:text-sm rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500"
            />
          </div>

          <div className="flex items-center gap-1.5 w-full sm:w-auto overflow-x-auto pb-1 sm:pb-0">
            <span className="text-xs font-semibold text-slate-500 flex items-center gap-1 mr-1">
              <Filter className="w-3.5 h-3.5" /> Budget:
            </span>
            {BUDGET_OPTIONS.map((opt) => (
              <button
                key={opt.label}
                onClick={() => setSelectedBudget(opt.value)}
                className={`px-3 py-1 rounded-lg text-xs font-semibold whitespace-nowrap transition-all ${
                  selectedBudget === opt.value
                    ? 'bg-indigo-600 text-white shadow-sm'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                {opt.label}
              </button>
            ))}
          </div>
        </div>

        {/* Category Filter Pills */}
        <div className="flex items-center gap-2 overflow-x-auto pt-2 border-t border-slate-100 pb-1">
          {CATEGORIES.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3.5 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition-all ${
                selectedCategory === cat
                  ? 'bg-slate-900 text-white shadow-sm'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              {cat === 'all' ? 'All Products' : cat}
            </button>
          ))}
        </div>
      </div>

      {/* Product Grid */}
      {loading ? (
        <div className="py-20 text-center">
          <div className="inline-block w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-xs text-slate-500 mt-2 font-medium">Loading catalog products...</p>
        </div>
      ) : products.length === 0 ? (
        <div className="bg-white rounded-2xl border border-dashed border-slate-300 p-12 text-center">
          <p className="text-slate-600 font-semibold text-base mb-1">No products found</p>
          <p className="text-slate-400 text-xs">Try adjusting your filters or ask our AI Salesman for assistance.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
          {products.map((product) => (
            <ProductCard
              key={product.id}
              product={product}
              onAddToCart={onAddToCart}
              onAskAI={(p) => onAskAI({ name: `Tell me about ${p.name}` })}
              onSelectForCompare={onSelectForCompare}
              isComparing={compareItems.some(i => i.id === product.id)}
            />
          ))}
        </div>
      )}
    </div>
  );
}
