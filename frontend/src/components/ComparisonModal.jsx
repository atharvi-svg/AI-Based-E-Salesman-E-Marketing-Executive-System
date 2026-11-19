import React from 'react';
import { X, Check, ShoppingCart, Scale } from 'lucide-react';

export default function ComparisonModal({
  comparisonData,
  isOpen,
  onClose,
  onAddToCart
}) {
  if (!isOpen || !comparisonData) return null;

  const { product_a, product_b, price_difference, cheaper_product_id, spec_matrix } = comparisonData;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
      <div className="bg-white rounded-3xl max-w-4xl w-full max-h-[90vh] flex flex-col shadow-2xl border border-slate-100 overflow-hidden">
        {/* Header */}
        <div className="p-5 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center">
              <Scale className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-slate-900">Side-by-Side Product Comparison</h2>
              <p className="text-xs text-slate-500">FR-PROD-02 • Comparing key specifications and pricing</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-xl text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-6 overflow-y-auto space-y-6">
          {/* Product Header Cards Side-by-Side */}
          <div className="grid grid-cols-2 gap-4 sm:gap-6">
            {/* Product A */}
            <div className={`p-4 rounded-2xl border ${cheaper_product_id === product_a.id ? 'border-emerald-300 bg-emerald-50/20' : 'border-slate-200 bg-white'}`}>
              <div className="h-32 rounded-xl overflow-hidden mb-3 bg-slate-100">
                <img
                  src={product_a.image_url || 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500&auto=format&fit=crop&q=60'}
                  alt={product_a.name}
                  className="w-full h-full object-cover"
                />
              </div>
              <h3 className="font-bold text-slate-900 text-sm sm:text-base mb-1 line-clamp-1">{product_a.name}</h3>
              <div className="flex items-center justify-between mb-3">
                <span className="text-lg font-black text-indigo-600">${product_a.price.toFixed(2)}</span>
                {cheaper_product_id === product_a.id && (
                  <span className="text-[10px] font-bold text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded-full">
                    Saves ${price_difference.toFixed(2)}
                  </span>
                )}
              </div>
              <button
                onClick={() => onAddToCart(product_a)}
                className="w-full py-2 px-3 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold flex items-center justify-center gap-1.5 transition-all shadow-sm"
              >
                <ShoppingCart className="w-3.5 h-3.5" />
                <span>Add {product_a.name.split(' ')[0]} to Cart</span>
              </button>
            </div>

            {/* Product B */}
            <div className={`p-4 rounded-2xl border ${cheaper_product_id === product_b.id ? 'border-emerald-300 bg-emerald-50/20' : 'border-slate-200 bg-white'}`}>
              <div className="h-32 rounded-xl overflow-hidden mb-3 bg-slate-100">
                <img
                  src={product_b.image_url || 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500&auto=format&fit=crop&q=60'}
                  alt={product_b.name}
                  className="w-full h-full object-cover"
                />
              </div>
              <h3 className="font-bold text-slate-900 text-sm sm:text-base mb-1 line-clamp-1">{product_b.name}</h3>
              <div className="flex items-center justify-between mb-3">
                <span className="text-lg font-black text-indigo-600">${product_b.price.toFixed(2)}</span>
                {cheaper_product_id === product_b.id && (
                  <span className="text-[10px] font-bold text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded-full">
                    Saves ${price_difference.toFixed(2)}
                  </span>
                )}
              </div>
              <button
                onClick={() => onAddToCart(product_b)}
                className="w-full py-2 px-3 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold flex items-center justify-center gap-1.5 transition-all shadow-sm"
              >
                <ShoppingCart className="w-3.5 h-3.5" />
                <span>Add {product_b.name.split(' ')[0]} to Cart</span>
              </button>
            </div>
          </div>

          {/* Specifications Matrix Table */}
          <div className="border border-slate-200 rounded-2xl overflow-hidden">
            <div className="bg-slate-100/70 px-4 py-2.5 font-bold text-xs text-slate-700 uppercase tracking-wider">
              Technical Specifications Comparison
            </div>
            <div className="divide-y divide-slate-100 text-xs sm:text-sm">
              <div className="grid grid-cols-3 p-3 bg-slate-50/50 font-bold text-slate-500 text-xs">
                <span>Feature</span>
                <span>{product_a.name}</span>
                <span>{product_b.name}</span>
              </div>
              {spec_matrix?.map((row, idx) => (
                <div
                  key={idx}
                  className={`grid grid-cols-3 p-3 items-center ${
                    row.different ? 'bg-amber-50/30 font-medium' : ''
                  }`}
                >
                  <span className="font-semibold text-slate-600">{row.feature}</span>
                  <span className="text-slate-800 pr-2">{String(row.product_a)}</span>
                  <span className="text-slate-800">{String(row.product_b)}</span>
                </div>
              ))}
              <div className="grid grid-cols-3 p-3 items-center bg-slate-50/80">
                <span className="font-bold text-slate-700">Stock Availability</span>
                <span className="text-emerald-700 font-semibold">{product_a.stock_status}</span>
                <span className="text-emerald-700 font-semibold">{product_b.stock_status}</span>
              </div>
              <div className="grid grid-cols-3 p-3 items-center bg-slate-50/80">
                <span className="font-bold text-slate-700">Promotions</span>
                <span className="text-rose-600 font-semibold">{product_a.offer_flag || 'None'}</span>
                <span className="text-rose-600 font-semibold">{product_b.offer_flag || 'None'}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
