import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import ProductCatalog from './components/ProductCatalog';
import ComparisonModal from './components/ComparisonModal';
import CartModal from './components/CartModal';
import ChatAssistant from './components/ChatAssistant';
import AdminDashboard from './components/AdminDashboard';
import { fetchProducts, recordAddToCart, compareProducts, completeCheckout } from './services/api';

export default function App() {
  const [activeView, setActiveView] = useState('store');
  const [sessionId, setSessionId] = useState(() => {
    const existing = localStorage.getItem('ai_salesman_session_id');
    if (existing) return existing;
    const newId = 'session_' + Math.random().toString(36).substring(2, 9) + '_' + Date.now().toString().slice(-4);
    localStorage.setItem('ai_salesman_session_id', newId);
    return newId;
  });

  const [products, setProducts] = useState([]);
  const [loadingProducts, setLoadingProducts] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedBudget, setSelectedBudget] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');

  const [cart, setCart] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem('ai_salesman_cart') || '[]');
    } catch {
      return [];
    }
  });

  const [leadScore, setLeadScore] = useState(0);
  const [leadStatus, setLeadStatus] = useState('Cold');

  const [isCartOpen, setIsCartOpen] = useState(false);
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [externalPrompt, setExternalPrompt] = useState('');

  const [compareItems, setCompareItems] = useState([]);
  const [comparisonData, setComparisonData] = useState(null);
  const [isCompareModalOpen, setIsCompareModalOpen] = useState(false);

  // Save cart to local storage
  useEffect(() => {
    localStorage.setItem('ai_salesman_cart', JSON.stringify(cart));
  }, [cart]);

  // Load products from API
  const loadProducts = async () => {
    setLoadingProducts(true);
    try {
      const data = await fetchProducts({
        category: selectedCategory,
        budget: selectedBudget,
        search: searchQuery
      });
      setProducts(data);
    } catch (err) {
      console.error('Failed to load products:', err);
    } finally {
      setLoadingProducts(false);
    }
  };

  useEffect(() => {
    loadProducts();
  }, [selectedCategory, selectedBudget, searchQuery]);

  // Sync initial lead status for this session
  useEffect(() => {
    async function syncLead() {
      try {
        const res = await fetch(`http://127.0.0.1:8000/api/admin/leads`);
        if (res.ok) {
          const leads = await res.json();
          const current = leads.find(l => l.session_id === sessionId);
          if (current) {
            setLeadScore(current.score);
            setLeadStatus(current.status);
          }
        }
      } catch (e) {
        // backend loading
      }
    }
    syncLead();
  }, [sessionId]);

  // Handle Add to Cart (FR-PUR-01, FR-LEAD-02: +15)
  const handleAddToCart = async (product) => {
    setCart(prev => {
      const existing = prev.find(item => item.id === product.id);
      if (existing) {
        return prev.map(item => item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item);
      }
      return [...prev, { ...product, quantity: 1 }];
    });

    try {
      const res = await recordAddToCart({
        session_id: sessionId,
        product_id: product.id,
        quantity: 1
      });
      if (res.lead_score !== undefined) {
        setLeadScore(res.lead_score);
        setLeadStatus(res.lead_status);
      }
    } catch (err) {
      console.error('Failed to record add to cart score:', err);
    }
  };

  const handleUpdateQuantity = (productId, newQuantity) => {
    if (newQuantity <= 0) {
      handleRemoveItem(productId);
      return;
    }
    setCart(prev => prev.map(item => item.id === productId ? { ...item, quantity: newQuantity } : item));
  };

  const handleRemoveItem = (productId) => {
    setCart(prev => prev.filter(item => item.id !== productId));
  };

  const handleClearCart = () => {
    setCart([]);
  };

  // Handle Product Selection for Compare
  const handleSelectForCompare = (product) => {
    setCompareItems(prev => {
      const exists = prev.find(p => p.id === product.id);
      if (exists) {
        return prev.filter(p => p.id !== product.id);
      }
      if (prev.length >= 2) {
        return [prev[1], product]; // keep last and add new
      }
      return [...prev, product];
    });
  };

  // Trigger Side-by-Side Comparison
  const handleTriggerCompare = async () => {
    if (compareItems.length < 2) return;
    try {
      const data = await compareProducts(compareItems[0].id, compareItems[1].id);
      setComparisonData(data);
      setIsCompareModalOpen(true);

      // Score +10 for compare action
      const res = await fetch('http://127.0.0.1:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          message: `Compare ${compareItems[0].name} and ${compareItems[1].name}`
        })
      });
      if (res.ok) {
        const chatRes = await res.json();
        setLeadScore(chatRes.lead_score);
        setLeadStatus(chatRes.lead_status);
      }
    } catch (err) {
      alert('Failed to compare products: ' + err.message);
    }
  };

  // Handle Asking AI about a product
  const handleAskAI = (item) => {
    setIsChatOpen(true);
    setExternalPrompt(item.name ? `Tell me more about ${item.name}` : item);
  };

  // Handle Reset Test Session (for evaluator convenience)
  const handleResetSession = () => {
    const newId = 'session_' + Math.random().toString(36).substring(2, 9) + '_' + Date.now().toString().slice(-4);
    localStorage.setItem('ai_salesman_session_id', newId);
    setSessionId(newId);
    setCart([]);
    setLeadScore(0);
    setLeadStatus('Cold');
    setCompareItems([]);
    alert(`Fresh test session started! Session ID: ${newId}\nLead score reset to 0 (Cold).`);
  };

  // Handle Simulated Checkout
  const handleCheckoutComplete = async (orderPayload) => {
    const result = await completeCheckout(orderPayload);
    // After checkout, lead is converted!
    setLeadScore(prev => prev);
    return result;
  };

  const cartCount = cart.reduce((total, item) => total + item.quantity, 0);

  return (
    <div className="min-h-screen flex flex-col bg-slate-50">
      {/* Top Navigation */}
      <Navbar
        activeView={activeView}
        setActiveView={setActiveView}
        cartCount={cartCount}
        onOpenCart={() => setIsCartOpen(true)}
        leadScore={leadScore}
        leadStatus={leadStatus}
        onResetSession={handleResetSession}
        sessionId={sessionId}
        isChatOpen={isChatOpen}
        setIsChatOpen={setIsChatOpen}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {activeView === 'store' ? (
          <ProductCatalog
            products={products}
            loading={loadingProducts}
            selectedCategory={selectedCategory}
            setSelectedCategory={setSelectedCategory}
            selectedBudget={selectedBudget}
            setSelectedBudget={setSelectedBudget}
            searchQuery={searchQuery}
            setSearchQuery={setSearchQuery}
            onAddToCart={handleAddToCart}
            onAskAI={handleAskAI}
            compareItems={compareItems}
            onSelectForCompare={handleSelectForCompare}
            onTriggerCompare={handleTriggerCompare}
            onClearCompare={() => setCompareItems([])}
          />
        ) : (
          <AdminDashboard currentSessionId={sessionId} />
        )}
      </main>

      {/* Floating Chat Assistant Widget */}
      <ChatAssistant
        isOpen={isChatOpen}
        onClose={() => setIsChatOpen(false)}
        sessionId={sessionId}
        leadScore={leadScore}
        leadStatus={leadStatus}
        onAddToCart={handleAddToCart}
        onSelectForCompare={handleSelectForCompare}
        externalPrompt={externalPrompt}
        onClearExternalPrompt={() => setExternalPrompt('')}
        onScoreUpdated={(score, status) => {
          setLeadScore(score);
          setLeadStatus(status);
        }}
      />

      {/* Comparison Modal */}
      <ComparisonModal
        isOpen={isCompareModalOpen}
        onClose={() => setIsCompareModalOpen(false)}
        comparisonData={comparisonData}
        onAddToCart={handleAddToCart}
      />

      {/* Cart & Checkout Modal */}
      <CartModal
        isOpen={isCartOpen}
        onClose={() => setIsCartOpen(false)}
        items={cart}
        onUpdateQuantity={handleUpdateQuantity}
        onRemoveItem={handleRemoveItem}
        onClearCart={handleClearCart}
        onCheckoutComplete={handleCheckoutComplete}
        sessionId={sessionId}
      />

      {/* Footer */}
      <footer className="mt-auto border-t border-slate-200 bg-white py-6">
        <div className="max-w-7xl mx-auto px-4 text-center text-xs text-slate-500 space-y-1">
          <p className="font-semibold text-slate-700">
            AI-Based E-Salesman & E-Marketing Executive System • Version 2.0
          </p>
          <p>
            UE24CS341A Software Engineering Mini-Project • Team Code Connect (Project ID: 15)
          </p>
          <p className="text-[11px] text-slate-400">
            Atharvi • Chandana • Harika • Arun
          </p>
        </div>
      </footer>
    </div>
  );
}
