import React from 'react';
import { ShoppingCart, MessageSquare, Star, CheckCircle, AlertCircle, Scale } from 'lucide-react';

export default function ProductCard({
  product,
  onAddToCart,
  onAskAI,
  onSelectForCompare,
  isComparing
}) {
  const isOutOfStock = product.stock_status === 'Out of Stock';

  return (
    <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm hover:shadow-md transition-all flex flex-col group">
      {/* Product Image Header */}
      <div className="relative h-48 bg-slate-100 overflow-hidden">
        <img
          src={product.image_url || 'https://images.unsplash.com/photo-1526738549149-8e07eca6c147?w=500&auto=format&fit=crop&q=60'}
          alt={product.name}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          loading="lazy"
        />
        <div className="absolute top-2.5 left-2.5 flex flex-col gap-1.5 items-start">
          <span className="text-[11px] font-semibold px-2 py-0.5 rounded-md bg-white/90 backdrop-blur text-slate-800 shadow-sm border border-slate-200">
            {product.category}
          </span>
          {product.is_featured && (
            <span className="flex items-center gap-1 text-[11px] font-bold px-2 py-0.5 rounded-md bg-amber-500 text-white shadow-sm">
              <Star className="w-3 h-3 fill-current" /> Featured
            </span>
          )}
        </div>
        {product.offer_flag && (
          <div className="absolute top-2.5 right-2.5 bg-rose-600 text-white text-[11px] font-bold px-2.5 py-0.5 rounded-full shadow-sm animate-pulse">
            {product.offer_flag}
          </div>
        )}
      </div>

      {/* Product Details */}
      <div className="p-4 flex-1 flex flex-col justify-between">
        <div>
          <div className="flex items-start justify-between gap-2 mb-1">
            <h3 className="font-bold text-slate-900 text-base group-hover:text-indigo-600 transition-colors line-clamp-1">
              {product.name}
            </h3>
            <span className="font-extrabold text-indigo-600 text-base whitespace-nowrap">
              ${product.price.toFixed(2)}
            </span>
          </div>

          <p className="text-xs text-slate-500 line-clamp-2 mb-3">
            {product.description}
          </p>

          {/* Key Specs Pills */}
          <div className="flex flex-wrap gap-1.5 mb-3">
            {Object.entries(product.specs || {}).slice(0, 3).map(([key, val]) => (
              <span
                key={key}
                className="text-[10px] font-medium bg-slate-50 border border-slate-100 text-slate-600 px-2 py-0.5 rounded"
              >
                <strong className="capitalize">{key.replace('_', ' ')}:</strong> {String(val).slice(0, 18)}
              </span>
            ))}
          </div>

          {/* Stock Status */}
          <div className="flex items-center gap-1.5 text-xs font-medium text-slate-600 mb-4">
            {isOutOfStock ? (
              <>
                <AlertCircle className="w-3.5 h-3.5 text-rose-500" />
                <span className="text-rose-600 font-semibold">Out of Stock</span>
              </>
            ) : product.stock_status === 'Limited Stock' ? (
              <>
                <AlertCircle className="w-3.5 h-3.5 text-amber-500" />
                <span className="text-amber-600 font-semibold">Limited Stock Available</span>
              </>
            ) : (
              <>
                <CheckCircle className="w-3.5 h-3.5 text-emerald-500" />
                <span className="text-emerald-700 font-semibold">In Stock</span>
              </>
            )}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="pt-2 border-t border-slate-100 flex items-center gap-2">
          <button
            onClick={() => onAddToCart(product)}
            disabled={isOutOfStock}
            className={`flex-1 py-2 px-3 rounded-xl text-xs font-semibold flex items-center justify-center gap-1.5 transition-all ${
              isOutOfStock
                ? 'bg-slate-100 text-slate-400 cursor-not-allowed'
                : 'bg-indigo-600 hover:bg-indigo-700 text-white shadow-sm shadow-indigo-100'
            }`}
          >
            <ShoppingCart className="w-3.5 h-3.5" />
            <span>Add to Cart</span>
          </button>

          <button
            onClick={() => onAskAI(product)}
            title="Ask AI Salesman about this product"
            className="p-2 rounded-xl border border-slate-200 text-slate-600 hover:text-indigo-600 hover:bg-indigo-50/50 hover:border-indigo-200 transition-all"
          >
            <MessageSquare className="w-4 h-4" />
          </button>

          <button
            onClick={() => onSelectForCompare(product)}
            title="Select to compare with another product"
            className={`p-2 rounded-xl border transition-all ${
              isComparing
                ? 'bg-indigo-50 text-indigo-600 border-indigo-300'
                : 'border-slate-200 text-slate-600 hover:text-indigo-600 hover:bg-indigo-50/50'
            }`}
          >
            <Scale className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
