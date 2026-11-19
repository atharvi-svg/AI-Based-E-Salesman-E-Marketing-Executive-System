import React, { useState, useEffect } from 'react';
import {
  Users, Flame, ThermometerSun, Snowflake, DollarSign,
  TrendingUp, CheckCircle2, Clock, Search, Filter, ArrowUpDown,
  MessageSquare, ShoppingBag, Eye, X, RefreshCw
} from 'lucide-react';
import { fetchAdminMetrics, fetchAdminLeads, fetchAdminLeadDetails } from '../services/api';

export default function AdminDashboard({ currentSessionId }) {
  const [metrics, setMetrics] = useState({
    total_leads: 0,
    hot_leads: 0,
    warm_leads: 0,
    cold_leads: 0,
    total_conversions: 0,
    conversion_rate: 0,
    total_revenue: 0
  });
  const [leads, setLeads] = useState([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState('all');
  const [convertedFilter, setConvertedFilter] = useState('all');
  const [sortBy, setSortBy] = useState('score');
  const [sortOrder, setSortOrder] = useState('desc');
  const [selectedLead, setSelectedLead] = useState(null);
  const [leadDetailLoading, setLeadDetailLoading] = useState(false);

  const loadData = async () => {
    setLoading(true);
    try {
      const [m, l] = await Promise.all([
        fetchAdminMetrics(),
        fetchAdminLeads({
          status: statusFilter,
          converted: convertedFilter === 'all' ? null : convertedFilter === 'true',
          sort_by: sortBy,
          order: sortOrder
        })
      ]);
      setMetrics(m);
      setLeads(l);
    } catch (err) {
      console.error('Failed to load admin data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [statusFilter, convertedFilter, sortBy, sortOrder]);

  const handleOpenLead = async (leadId) => {
    setLeadDetailLoading(true);
    try {
      const details = await fetchAdminLeadDetails(leadId);
      setSelectedLead(details);
    } catch (err) {
      alert('Failed to load lead details: ' + err.message);
    } finally {
      setLeadDetailLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header & Refresh */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-black text-slate-900 tracking-tight">Internal CRM & Sales Lead Dashboard</h1>
            <span className="text-xs px-2.5 py-0.5 rounded-full font-bold bg-indigo-50 text-indigo-700 border border-indigo-200">
              FR-CRM-04
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-0.5">
            Monitor real-time sales prospects, conversation behavior scoring, lead classifications, and simulated order conversions.
          </p>
        </div>

        <button
          onClick={loadData}
          disabled={loading}
          className="px-3.5 py-2 rounded-xl bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-xs font-semibold flex items-center gap-2 shadow-2xs transition-all w-fit"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin text-indigo-600' : ''}`} />
          <span>Refresh Data</span>
        </button>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-6 gap-3 sm:gap-4">
        {/* Total Leads */}
        <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs">
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-semibold">Total Leads</span>
            <Users className="w-4 h-4 text-indigo-600" />
          </div>
          <p className="text-2xl font-black text-slate-900">{metrics.total_leads}</p>
          <p className="text-[11px] text-slate-400 mt-1">Tracked sessions</p>
        </div>

        {/* Hot Leads */}
        <div className="bg-white p-4 rounded-2xl border border-rose-100 bg-gradient-to-b from-rose-50/30 to-white shadow-xs">
          <div className="flex items-center justify-between text-rose-600 mb-2">
            <span className="text-xs font-bold">Hot Leads (35+)</span>
            <Flame className="w-4 h-4 fill-current text-rose-500" />
          </div>
          <p className="text-2xl font-black text-rose-600">{metrics.hot_leads}</p>
          <p className="text-[11px] text-rose-500/80 mt-1">High purchase intent</p>
        </div>

        {/* Warm Leads */}
        <div className="bg-white p-4 rounded-2xl border border-amber-100 bg-gradient-to-b from-amber-50/30 to-white shadow-xs">
          <div className="flex items-center justify-between text-amber-600 mb-2">
            <span className="text-xs font-bold">Warm Leads (15-34)</span>
            <ThermometerSun className="w-4 h-4 text-amber-500" />
          </div>
          <p className="text-2xl font-black text-amber-600">{metrics.warm_leads}</p>
          <p className="text-[11px] text-amber-600/80 mt-1">Comparing & engaged</p>
        </div>

        {/* Cold Leads */}
        <div className="bg-white p-4 rounded-2xl border border-blue-100 bg-gradient-to-b from-blue-50/30 to-white shadow-xs">
          <div className="flex items-center justify-between text-blue-600 mb-2">
            <span className="text-xs font-bold">Cold Leads (0-14)</span>
            <Snowflake className="w-4 h-4 text-blue-500" />
          </div>
          <p className="text-2xl font-black text-blue-600">{metrics.cold_leads}</p>
          <p className="text-[11px] text-blue-500/80 mt-1">Browsing visitors</p>
        </div>

        {/* Total Conversions */}
        <div className="bg-white p-4 rounded-2xl border border-emerald-100 bg-gradient-to-b from-emerald-50/30 to-white shadow-xs">
          <div className="flex items-center justify-between text-emerald-600 mb-2">
            <span className="text-xs font-bold">Conversions</span>
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          </div>
          <p className="text-2xl font-black text-emerald-700">{metrics.total_conversions}</p>
          <p className="text-[11px] text-emerald-600 mt-1">Rate: {metrics.conversion_rate}%</p>
        </div>

        {/* Total Simulated Revenue */}
        <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs">
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-semibold">Simulated Revenue</span>
            <DollarSign className="w-4 h-4 text-emerald-600" />
          </div>
          <p className="text-2xl font-black text-slate-900">${metrics.total_revenue.toFixed(0)}</p>
          <p className="text-[11px] text-slate-400 mt-1">Completed checkouts</p>
        </div>
      </div>

      {/* Leads Table Card with Filters */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">
        {/* Table Filters Bar */}
        <div className="p-4 border-b border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-slate-50/50">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-xs font-bold text-slate-500 flex items-center gap-1">
              <Filter className="w-3.5 h-3.5" /> Filter Status:
            </span>
            {['all', 'Hot', 'Warm', 'Cold'].map((st) => (
              <button
                key={st}
                onClick={() => setStatusFilter(st)}
                className={`px-2.5 py-1 rounded-lg text-xs font-semibold transition-all ${
                  statusFilter === st
                    ? 'bg-slate-900 text-white shadow-xs'
                    : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-100'
                }`}
              >
                {st === 'all' ? 'All Leads' : st}
              </button>
            ))}

            <div className="h-4 w-[1px] bg-slate-300 mx-1 hidden sm:block"></div>

            <span className="text-xs font-bold text-slate-500">Conversion:</span>
            <button
              onClick={() => setConvertedFilter(convertedFilter === 'true' ? 'all' : 'true')}
              className={`px-2.5 py-1 rounded-lg text-xs font-semibold transition-all ${
                convertedFilter === 'true'
                  ? 'bg-emerald-600 text-white shadow-xs'
                  : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-100'
              }`}
            >
              Converted Only
            </button>
          </div>

          {/* Sorting */}
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold text-slate-500 flex items-center gap-1">
              <ArrowUpDown className="w-3.5 h-3.5" /> Sort:
            </span>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="text-xs font-semibold px-2.5 py-1 rounded-lg border border-slate-200 bg-white text-slate-700 focus:outline-none"
            >
              <option value="score">Lead Score</option>
              <option value="last_interaction">Last Interaction</option>
              <option value="created_at">Created Date</option>
            </select>
            <button
              onClick={() => setSortOrder(sortOrder === 'desc' ? 'asc' : 'desc')}
              className="px-2 py-1 rounded-lg border border-slate-200 bg-white text-xs font-bold text-slate-700"
            >
              {sortOrder.toUpperCase()}
            </button>
          </div>
        </div>

        {/* Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs sm:text-sm">
            <thead className="bg-slate-50 border-b border-slate-200 text-slate-500 font-bold uppercase tracking-wider text-[11px]">
              <tr>
                <th className="py-3 px-4">Lead / Customer</th>
                <th className="py-3 px-4">Lead Score</th>
                <th className="py-3 px-4">Classification</th>
                <th className="py-3 px-4">Actions Triggered</th>
                <th className="py-3 px-4">Conversion</th>
                <th className="py-3 px-4">Last Activity</th>
                <th className="py-3 px-4 text-right">CRM Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {loading ? (
                <tr>
                  <td colSpan="7" className="py-12 text-center text-slate-400">
                    Loading CRM leads...
                  </td>
                </tr>
              ) : leads.length === 0 ? (
                <tr>
                  <td colSpan="7" className="py-12 text-center text-slate-400">
                    No leads found matching current filter.
                  </td>
                </tr>
              ) : (
                leads.map((lead) => {
                  const isCurrent = lead.session_id === currentSessionId;
                  return (
                    <tr
                      key={lead.id}
                      className={`hover:bg-slate-50/80 transition-colors ${
                        isCurrent ? 'bg-indigo-50/40' : ''
                      }`}
                    >
                      {/* Customer Name & Session ID */}
                      <td className="py-3.5 px-4">
                        <div className="font-bold text-slate-900">
                          {lead.name || 'Anonymous Visitor'}
                          {isCurrent && (
                            <span className="ml-2 text-[10px] bg-indigo-100 text-indigo-700 px-1.5 py-0.2 rounded font-bold">
                              Current Session
                            </span>
                          )}
                        </div>
                        <div className="text-[11px] text-slate-500 font-mono">
                          {lead.contact || lead.session_id}
                        </div>
                      </td>

                      {/* Score */}
                      <td className="py-3.5 px-4">
                        <div className="flex items-center gap-2">
                          <span className="font-extrabold text-base text-slate-900">{lead.score}</span>
                          <span className="text-[10px] text-slate-400">pts</span>
                        </div>
                        {/* Mini progress bar */}
                        <div className="w-20 h-1.5 bg-slate-100 rounded-full overflow-hidden mt-1">
                          <div
                            className={`h-full rounded-full ${
                              lead.score >= 35
                                ? 'bg-rose-500'
                                : lead.score >= 15
                                ? 'bg-amber-500'
                                : 'bg-blue-500'
                            }`}
                            style={{ width: `${Math.min(100, (lead.score / 50) * 100)}%` }}
                          />
                        </div>
                      </td>

                      {/* Status Badge */}
                      <td className="py-3.5 px-4">
                        <span
                          className={`inline-flex items-center gap-1 text-[11px] font-bold px-2.5 py-1 rounded-full uppercase tracking-wider ${
                            lead.status === 'Hot'
                              ? 'bg-rose-100 text-rose-700 border border-rose-200'
                              : lead.status === 'Warm'
                              ? 'bg-amber-100 text-amber-700 border border-amber-200'
                              : 'bg-blue-100 text-blue-700 border border-blue-200'
                          }`}
                        >
                          {lead.status === 'Hot' && <Flame className="w-3 h-3 fill-current" />}
                          {lead.status === 'Warm' && <ThermometerSun className="w-3 h-3" />}
                          {lead.status === 'Cold' && <Snowflake className="w-3 h-3" />}
                          {lead.status}
                        </span>
                      </td>

                      {/* Triggered Actions Breakdown */}
                      <td className="py-3.5 px-4">
                        <div className="flex flex-wrap gap-1 max-w-xs">
                          {lead.scored_actions?.length > 0 ? (
                            lead.scored_actions.map((act) => (
                              <span
                                key={act}
                                className="text-[10px] font-medium bg-slate-100 text-slate-700 px-2 py-0.5 rounded border border-slate-200"
                              >
                                {act === 'price_query' && '💰 Price (+5)'}
                                {act === 'compare_query' && '⚖️ Compare (+10)'}
                                {act === 'purchase_intent' && '🔥 Purchase (+20)'}
                                {act === 'added_to_cart' && '🛒 Cart (+15)'}
                                {act === 'viewed_3_products' && '👀 3+ Products (+5)'}
                              </span>
                            ))
                          ) : (
                            <span className="text-[11px] text-slate-400">None yet</span>
                          )}
                        </div>
                      </td>

                      {/* Conversion */}
                      <td className="py-3.5 px-4">
                        {lead.is_converted ? (
                          <span className="inline-flex items-center gap-1 text-xs font-bold text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200">
                            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" /> Converted
                          </span>
                        ) : (
                          <span className="text-xs font-medium text-slate-400">In Progress</span>
                        )}
                      </td>

                      {/* Last Activity */}
                      <td className="py-3.5 px-4 text-xs text-slate-500 whitespace-nowrap">
                        <div className="flex items-center gap-1">
                          <Clock className="w-3 h-3 text-slate-400" />
                          <span>{lead.last_interaction}</span>
                        </div>
                      </td>

                      {/* Actions */}
                      <td className="py-3.5 px-4 text-right">
                        <button
                          onClick={() => handleOpenLead(lead.id)}
                          className="px-3 py-1.5 rounded-xl bg-indigo-50 hover:bg-indigo-100 text-indigo-700 text-xs font-bold transition-all inline-flex items-center gap-1.5"
                        >
                          <Eye className="w-3.5 h-3.5" />
                          <span>Inspect</span>
                        </button>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Lead Detail & Transcript Drawer/Modal */}
      {selectedLead && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div className="bg-white rounded-3xl max-w-3xl w-full max-h-[90vh] flex flex-col shadow-2xl border border-slate-100 overflow-hidden">
            {/* Modal Header */}
            <div className="p-5 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-indigo-600 text-white flex items-center justify-center font-bold">
                  <Users className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-lg font-bold text-slate-900">
                    Lead Profile: {selectedLead.lead.name || 'Anonymous Lead'}
                  </h2>
                  <p className="text-xs text-slate-500 font-mono">
                    Session: {selectedLead.lead.session_id} • First Seen: {selectedLead.lead.created_at}
                  </p>
                </div>
              </div>
              <button
                onClick={() => setSelectedLead(null)}
                className="p-2 rounded-xl text-slate-400 hover:text-slate-700 hover:bg-slate-100"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Modal Content */}
            <div className="p-6 overflow-y-auto space-y-6">
              {/* Lead Summary Overview */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-slate-50 p-4 rounded-2xl border border-slate-200">
                <div>
                  <span className="text-[11px] text-slate-400 font-semibold uppercase">Lead Score</span>
                  <p className="text-xl font-black text-indigo-600">{selectedLead.lead.score} pts</p>
                </div>
                <div>
                  <span className="text-[11px] text-slate-400 font-semibold uppercase">Classification</span>
                  <p className="text-sm font-bold text-slate-800">{selectedLead.lead.status}</p>
                </div>
                <div>
                  <span className="text-[11px] text-slate-400 font-semibold uppercase">Conversion Status</span>
                  <p className={`text-sm font-bold ${selectedLead.lead.is_converted ? 'text-emerald-600' : 'text-slate-500'}`}>
                    {selectedLead.lead.is_converted ? '✅ Converted' : '⏳ Active'}
                  </p>
                </div>
                <div>
                  <span className="text-[11px] text-slate-400 font-semibold uppercase">Contact Details</span>
                  <p className="text-xs font-medium text-slate-800 truncate">
                    {selectedLead.lead.contact || 'Not provided'}
                  </p>
                </div>
              </div>

              {/* Orders placed by this lead if converted */}
              {selectedLead.orders?.length > 0 && (
                <div className="space-y-2">
                  <h4 className="font-bold text-slate-900 text-xs uppercase tracking-wider flex items-center gap-1.5">
                    <ShoppingBag className="w-4 h-4 text-emerald-600" />
                    Simulated Orders Placed ({selectedLead.orders.length})
                  </h4>
                  {selectedLead.orders.map((ord) => (
                    <div key={ord.id} className="p-3 bg-emerald-50/40 border border-emerald-200 rounded-xl text-xs space-y-1">
                      <div className="flex justify-between font-bold text-slate-800">
                        <span>Order #{ord.id}</span>
                        <span className="text-emerald-700">${ord.total_price.toFixed(2)}</span>
                      </div>
                      <div className="text-slate-500">
                        Items: {ord.product_ids?.map(i => `${i.name} (x${i.quantity})`).join(', ')}
                      </div>
                      <div className="text-[10px] text-slate-400">Date: {ord.created_at}</div>
                    </div>
                  ))}
                </div>
              )}

              {/* Full Conversation History Transcript */}
              <div className="space-y-3">
                <h4 className="font-bold text-slate-900 text-xs uppercase tracking-wider flex items-center gap-1.5">
                  <MessageSquare className="w-4 h-4 text-indigo-600" />
                  Full Chat Transcript (FR-CRM-02)
                </h4>
                <div className="bg-slate-50 rounded-2xl border border-slate-200 p-4 max-h-80 overflow-y-auto space-y-3">
                  {selectedLead.chat_logs?.length === 0 ? (
                    <p className="text-xs text-slate-400 text-center py-4">No chat logs recorded yet for this session.</p>
                  ) : (
                    selectedLead.chat_logs.map((log) => (
                      <div
                        key={log.id}
                        className={`flex flex-col ${log.sender === 'customer' ? 'items-end' : 'items-start'}`}
                      >
                        <div className="flex items-center gap-1.5 text-[10px] text-slate-400 mb-0.5 px-1">
                          <span className="font-bold capitalize">{log.sender}</span>
                          <span>• {log.timestamp}</span>
                          {log.intent && (
                            <span className="bg-indigo-50 text-indigo-600 px-1.5 py-0.2 rounded font-semibold border border-indigo-100">
                              {log.intent}
                            </span>
                          )}
                        </div>
                        <div
                          className={`p-3 rounded-2xl text-xs max-w-[85%] whitespace-pre-wrap leading-relaxed ${
                            log.sender === 'customer'
                              ? 'bg-indigo-600 text-white rounded-br-xs'
                              : 'bg-white text-slate-800 border border-slate-200 rounded-bl-xs'
                          }`}
                        >
                          {log.message}
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
