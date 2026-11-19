/**
 * Centralized API service for communicating with AI-Salesman FastAPI backend.
 */

const API_BASE = "http://127.0.0.1:8000/api";

export async function fetchProducts({ category = "all", budget = null, search = "" } = {}) {
  const params = new URLSearchParams();
  if (category && category !== "all") params.append("category", category);
  if (budget) params.append("budget", budget);
  if (search) params.append("search", search);

  const res = await fetch(`${API_BASE}/products?${params.toString()}`);
  if (!res.ok) throw new Error("Failed to load products");
  return await res.json();
}

export async function fetchProduct(id) {
  const res = await fetch(`${API_BASE}/products/${id}`);
  if (!res.ok) throw new Error("Product not found");
  return await res.json();
}

export async function compareProducts(id1, id2) {
  const res = await fetch(`${API_BASE}/products/compare?id1=${id1}&id2=${id2}`);
  if (!res.ok) throw new Error("Failed to compare products");
  return await res.json();
}

export async function sendChatMessage({ session_id, message, user_name, user_contact }) {
  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id, message, user_name, user_contact })
  });
  if (!res.ok) throw new Error("Chat request failed");
  return await res.json();
}

export async function fetchChatHistory(session_id) {
  const res = await fetch(`${API_BASE}/chat/history/${session_id}`);
  if (!res.ok) throw new Error("Failed to fetch chat history");
  return await res.json();
}

export async function recordAddToCart({ session_id, product_id, quantity = 1 }) {
  const res = await fetch(`${API_BASE}/cart/add`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id, product_id, quantity })
  });
  if (!res.ok) throw new Error("Failed to record cart addition");
  return await res.json();
}

export async function completeCheckout({ session_id, customer_name, customer_contact, items, total_price }) {
  const res = await fetch(`${API_BASE}/cart/checkout`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      session_id,
      customer_name,
      customer_contact,
      items,
      total_price
    })
  });
  if (!res.ok) throw new Error("Checkout failed");
  return await res.json();
}

export async function fetchAdminMetrics() {
  const res = await fetch(`${API_BASE}/admin/metrics`);
  if (!res.ok) throw new Error("Failed to load admin metrics");
  return await res.json();
}

export async function fetchAdminLeads({ status = "all", converted = null, sort_by = "score", order = "desc" } = {}) {
  const params = new URLSearchParams();
  if (status && status !== "all") params.append("status", status);
  if (converted !== null) params.append("converted", converted);
  params.append("sort_by", sort_by);
  params.append("order", order);

  const res = await fetch(`${API_BASE}/admin/leads?${params.toString()}`);
  if (!res.ok) throw new Error("Failed to fetch leads");
  return await res.json();
}

export async function fetchAdminLeadDetails(lead_id) {
  const res = await fetch(`${API_BASE}/admin/leads/${lead_id}`);
  if (!res.ok) throw new Error("Failed to fetch lead details");
  return await res.json();
}
