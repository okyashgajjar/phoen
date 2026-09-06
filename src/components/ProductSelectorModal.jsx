import React, { useState, useEffect, useMemo } from 'react';
import { api } from '../api';

function formatINR(value) {
  if (value === null || value === undefined) return '—';
  return `₹${Number(value).toLocaleString('en-IN', { maximumFractionDigits: 0 })}`;
}

export default function ProductSelectorModal({ isOpen, onClose, onAddLine, existingLines = [] }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedType, setSelectedType] = useState('');
  const [inStockOnly, setInStockOnly] = useState(false);

  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Selected item configuration state
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [selectedVariant, setSelectedVariant] = useState(null);
  const [productDetail, setProductDetail] = useState(null);
  const [loadingDetail, setLoadingDetail] = useState(false);

  // Form inputs
  const [qty, setQty] = useState(1);
  const [discountPercent, setDiscountPercent] = useState(0);
  const [adding, setAdding] = useState(false);
  const [successToast, setSuccessToast] = useState('');

  // Fetch catalog on mount or when search/category/type changes
  useEffect(() => {
    if (!isOpen) return;

    let isMounted = true;
    const timer = setTimeout(async () => {
      setLoading(true);
      setError(null);
      try {
        const filters = { limit: 100 };
        if (searchTerm.trim()) filters.search = searchTerm.trim();
        if (selectedCategory) filters.category_id = selectedCategory;
        if (selectedType) filters.item_type = selectedType;

        const res = await api.getCatalog(filters);
        if (isMounted) {
          setProducts(res.products || []);
          if (res.categories && res.categories.length > 0) {
            setCategories(prev => (prev.length === 0 ? res.categories : prev));
          }
        }
      } catch (err) {
        if (isMounted) setError(err.message || 'Failed to load products');
      } finally {
        if (isMounted) setLoading(false);
      }
    }, 250);

    return () => {
      isMounted = false;
      clearTimeout(timer);
    };
  }, [isOpen, searchTerm, selectedCategory, selectedType]);

  // When a product is selected, fetch its detail with variants & warehouse stock
  const handleSelectProduct = async (prod) => {
    setSelectedProduct(prod);
    setSelectedVariant(null);
    setQty(1);
    setDiscountPercent(0);
    setLoadingDetail(true);

    try {
      const detail = await api.getProductDetail(prod.id);
      setProductDetail(detail);
      if (detail.variants && detail.variants.length > 0) {
        setSelectedVariant(detail.variants[0]);
      }
    } catch {
      setProductDetail(null);
    } finally {
      setLoadingDetail(false);
    }
  };

  // Close modal on Escape
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  // Filtered by in-stock if toggled
  const filteredProducts = useMemo(() => {
    if (!inStockOnly) return products;
    return products.filter((p) => {
      if (p.item_type === 'SERVICE' || p.item_type === 'SUBSCRIPTION') return true;
      return (p.stock_available || 0) > 0;
    });
  }, [products, inStockOnly]);

  // Calculations for selected item
  const currentUnitPrice = useMemo(() => {
    if (selectedVariant && selectedVariant.selling_price) {
      return Number(selectedVariant.selling_price);
    }
    if (selectedProduct) {
      return Number(selectedProduct.base_price || 0);
    }
    return 0;
  }, [selectedProduct, selectedVariant]);

  const lineSubtotal = qty * currentUnitPrice;
  const lineDiscountAmount = lineSubtotal * (Number(discountPercent || 0) / 100);
  const lineNetTotal = Math.max(0, lineSubtotal - lineDiscountAmount);

  const isHardwareHighDiscount = useMemo(() => {
    const isHw =
      selectedProduct &&
      (selectedProduct.category?.toLowerCase().includes('laptop') ||
        selectedProduct.category?.toLowerCase().includes('computing') ||
        selectedProduct.category?.toLowerCase().includes('desktop') ||
        selectedProduct.category?.toLowerCase().includes('infrastructure') ||
        selectedProduct.item_type === 'PRODUCT');
    return isHw && Number(discountPercent) > 15;
  }, [selectedProduct, discountPercent]);

  const handleAddCurrentLine = async () => {
    if (!selectedProduct) return;
    setAdding(true);
    try {
      const productIdToAdd = selectedVariant ? selectedVariant.id : selectedProduct.id;
      const itemName = selectedVariant ? selectedVariant.name : selectedProduct.name;

      await onAddLine({
        product_id: productIdToAdd,
        variant_id: selectedVariant ? selectedVariant.id : null,
        name: itemName,
        category: selectedProduct.category || selectedProduct.item_type,
        quantity: qty,
        unit_price: currentUnitPrice,
        discount_percent: Number(discountPercent || 0),
        is_recurring: selectedProduct.is_recurring || false,
      });

      setSuccessToast(`Added ${itemName} to quotation!`);
      setTimeout(() => setSuccessToast(''), 3000);
      setSelectedProduct(null);
      setSelectedVariant(null);
      setProductDetail(null);
    } catch (err) {
      setError(err.message || 'Failed to add line to quote');
    } finally {
      setAdding(false);
    }
  };

  const handleQuickAdd = async (e, prod) => {
    e.stopPropagation();
    try {
      await onAddLine({
        product_id: prod.id,
        name: prod.name,
        category: prod.category || prod.item_type,
        quantity: 1,
        unit_price: prod.base_price,
        discount_percent: 0.0,
        is_recurring: prod.is_recurring || false,
      });
      setSuccessToast(`Added ${prod.name} (1 unit) to quote!`);
      setTimeout(() => setSuccessToast(''), 3000);
    } catch (err) {
      setError(err.message || 'Failed to quick add item');
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 animate-in fade-in duration-200">
      <div className="bg-white w-full max-w-6xl rounded-2xl shadow-2xl border border-[#DEE2E6] flex flex-col max-h-[92vh] overflow-hidden">
        
        {/* Header */}
        <div className="px-6 py-4 border-b border-[#DEE2E6] flex items-center justify-between bg-[#FBF9FA]">
          <div>
            <div className="flex items-center gap-2">
              <span className="material-symbols-outlined text-[#714B67] text-[22px]">inventory_2</span>
              <h2 className="text-lg font-extrabold text-[#212529] tracking-tight">Enterprise Product Catalog</h2>
              <span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-[#EFE6ED] text-[#714B67]">
                PostgreSQL Live Database
              </span>
            </div>
            <p className="text-xs text-[#6C757D] mt-0.5">
              Search 450+ enterprise hardware SKUs, cloud software, and deployment SLA services
            </p>
          </div>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-lg flex items-center justify-center text-[#6C757D] hover:text-[#212529] hover:bg-[#F1F1F1] transition-colors"
          >
            <span className="material-symbols-outlined text-[20px]">close</span>
          </button>
        </div>

        {/* Success Toast */}
        {successToast && (
          <div className="bg-emerald-600 text-white px-6 py-2.5 text-xs font-bold flex items-center justify-between shadow-md transition-all">
            <span className="flex items-center gap-2">
              <span className="material-symbols-outlined text-[16px]">check_circle</span>
              {successToast}
            </span>
            <button onClick={() => setSuccessToast('')} className="text-emerald-100 hover:text-white text-xs">
              Dismiss
            </button>
          </div>
        )}

        {/* Search & Filter Bar */}
        <div className="p-5 border-b border-[#DEE2E6] bg-white flex flex-col gap-3">
          <div className="flex flex-col md:flex-row gap-3 items-stretch md:items-center justify-between">
            
            {/* Search Input */}
            <div className="relative flex-1">
              <span className="material-symbols-outlined absolute left-3.5 top-1/2 -translate-y-1/2 text-[#6C757D] text-[18px]">
                search
              </span>
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search by product name, SKU code (e.g. LAP-001, SRV-005), brand, or specs..."
                className="w-full pl-10 pr-9 py-2.5 text-xs font-medium rounded-xl border border-[#DEE2E6] focus:border-[#714B67] focus:ring-2 focus:ring-[#714B67]/20 outline-none transition-all placeholder:text-[#ADB5BD]"
                autoFocus
              />
              {searchTerm && (
                <button
                  onClick={() => setSearchTerm('')}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-[#6C757D] hover:text-[#212529]"
                >
                  <span className="material-symbols-outlined text-[16px]">cancel</span>
                </button>
              )}
            </div>

            {/* Type Filter */}
            <div className="flex items-center gap-2">
              <select
                value={selectedType}
                onChange={(e) => setSelectedType(e.target.value)}
                className="px-3 py-2 text-xs font-semibold rounded-xl border border-[#DEE2E6] bg-white text-[#212529] focus:outline-none focus:ring-2 focus:ring-[#714B67]/20"
              >
                <option value="">All Item Types</option>
                <option value="PRODUCT">Physical Products</option>
                <option value="SERVICE">Professional Services</option>
                <option value="SUBSCRIPTION">Recurring Subscriptions</option>
              </select>

              <label className="flex items-center gap-1.5 text-xs font-semibold text-[#4A4A4A] cursor-pointer select-none px-3 py-2 rounded-xl border border-[#DEE2E6] hover:bg-[#F8F9FA] transition-colors">
                <input
                  type="checkbox"
                  checked={inStockOnly}
                  onChange={(e) => setInStockOnly(e.target.checked)}
                  className="rounded border-[#DEE2E6] text-[#714B67] focus:ring-[#714B67]/20"
                />
                In Stock Only
              </label>
            </div>
          </div>

          {/* Category Filter Pills */}
          <div className="flex items-center gap-1.5 overflow-x-auto pb-1 text-xs no-scrollbar">
            <button
              onClick={() => setSelectedCategory('')}
              className={`px-3 py-1 rounded-lg font-bold shrink-0 transition-colors ${
                selectedCategory === ''
                  ? 'bg-[#714B67] text-white'
                  : 'bg-[#F1F3F5] text-[#495057] hover:bg-[#E9ECEF]'
              }`}
            >
              All Categories
            </button>
            {categories.map((cat) => (
              <button
                key={cat.id}
                onClick={() => setSelectedCategory(cat.id)}
                className={`px-3 py-1 rounded-lg font-bold shrink-0 transition-colors ${
                  selectedCategory === cat.id
                    ? 'bg-[#714B67] text-white'
                    : 'bg-[#F1F3F5] text-[#495057] hover:bg-[#E9ECEF]'
                }`}
              >
                {cat.name}
              </button>
            ))}
          </div>
        </div>

        {/* Content Area: Two Column Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-12 flex-1 overflow-hidden">
          
          {/* Left / Main: Products Table (8 cols) */}
          <div className="lg:col-span-7 xl:col-span-8 overflow-y-auto p-5 border-r border-[#DEE2E6] flex flex-col gap-3">
            <div className="flex items-center justify-between text-xs text-[#6C757D] px-1 font-semibold">
              <span>Showing {filteredProducts.length} items</span>
              <span>Click a product to configure variant &amp; commercial terms</span>
            </div>

            {loading && (
              <div className="py-16 text-center text-xs text-[#6C757D] flex flex-col items-center gap-2">
                <span className="material-symbols-outlined animate-spin text-[24px] text-[#714B67]">sync</span>
                Loading enterprise product catalog…
              </div>
            )}

            {!loading && error && (
              <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-xs text-rose-800">
                {error}
              </div>
            )}

            {!loading && !error && filteredProducts.length === 0 && (
              <div className="py-16 text-center text-xs text-[#6C757D]">
                No products found matching "{searchTerm}". Try a different search term or clear category filters.
              </div>
            )}

            {!loading && !error && filteredProducts.map((prod) => {
              const isSelected = selectedProduct?.id === prod.id;
              const isAlreadyInQuote = existingLines.some(
                (l) => (l.product_id || l.sku) === prod.id || (l.product_id || l.sku) === prod.code
              );

              return (
                <div
                  key={prod.id}
                  onClick={() => handleSelectProduct(prod)}
                  className={`border rounded-xl p-3.5 flex flex-col gap-2 cursor-pointer transition-all ${
                    isSelected
                      ? 'border-[#714B67] bg-[#FAF6F9] ring-2 ring-[#714B67]/20'
                      : 'border-[#DEE2E6] bg-white hover:border-[#ADB5BD] hover:bg-[#FAFAFA]'
                  }`}
                >
                  <div className="flex items-start justify-between gap-3">
                    <div className="flex flex-col">
                      <div className="flex items-center gap-2">
                        <span className="font-mono text-[11px] font-bold text-[#714B67] bg-[#F3EBF0] px-2 py-0.5 rounded">
                          {prod.code || prod.id}
                        </span>
                        {prod.brand && (
                          <span className="text-[11px] font-bold text-[#495057] uppercase tracking-wider">
                            {prod.brand}
                          </span>
                        )}
                        <span
                          className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                            prod.item_type === 'SERVICE'
                              ? 'bg-blue-50 text-blue-700'
                              : prod.item_type === 'SUBSCRIPTION'
                              ? 'bg-purple-50 text-purple-700'
                              : 'bg-emerald-50 text-emerald-700'
                          }`}
                        >
                          {prod.item_type}
                        </span>
                        {isAlreadyInQuote && (
                          <span className="text-[10px] font-bold bg-amber-50 text-amber-800 px-2 py-0.5 rounded-full">
                            In Quote
                          </span>
                        )}
                      </div>
                      <h4 className="text-xs font-bold text-[#212529] mt-1 leading-snug">{prod.name}</h4>
                      <span className="text-[11px] text-[#6C757D]">{prod.category || 'General'}</span>
                    </div>

                    <div className="flex flex-col items-end shrink-0">
                      <span className="font-mono font-extrabold text-sm text-[#212529]">
                        {formatINR(prod.base_price)}
                      </span>
                      <span className="text-[10px] font-bold text-emerald-700">
                        Margin {prod.margin_percent || 0}%
                      </span>
                    </div>
                  </div>

                  <div className="flex items-center justify-between pt-1 border-t border-[#F1F1F1] text-[11px]">
                    <div className="flex items-center gap-3">
                      {/* Live Stock Indicator */}
                      {prod.item_type === 'SERVICE' || prod.item_type === 'SUBSCRIPTION' ? (
                        <span className="text-emerald-700 font-semibold flex items-center gap-1">
                          <span className="material-symbols-outlined text-[13px]">cloud_done</span>
                          Digital Provisioning
                        </span>
                      ) : (prod.stock_available || 0) > 0 ? (
                        <span className="text-emerald-700 font-semibold flex items-center gap-1">
                          <span className="material-symbols-outlined text-[13px]">check_circle</span>
                          {prod.stock_available} units available across DCs
                        </span>
                      ) : (
                        <span className="text-rose-600 font-semibold flex items-center gap-1">
                          <span className="material-symbols-outlined text-[13px]">warning</span>
                          Backorder / 0 Free Stock
                        </span>
                      )}

                      {prod.variant_count > 0 && (
                        <span className="text-[#6C757D] font-medium flex items-center gap-0.5">
                          <span className="material-symbols-outlined text-[13px]">tune</span>
                          {prod.variant_count} Variants
                        </span>
                      )}
                    </div>

                    <div className="flex items-center gap-2">
                      <button
                        onClick={(e) => handleQuickAdd(e, prod)}
                        className="px-2.5 py-1 rounded-lg bg-[#F8F9FA] hover:bg-[#E9ECEF] text-[#495057] font-bold text-[11px] border border-[#DEE2E6] transition-colors"
                        title="Quick add 1 unit at base price"
                      >
                        + Quick Add
                      </button>
                      <button
                        onClick={() => handleSelectProduct(prod)}
                        className={`px-3 py-1 rounded-lg font-bold text-[11px] transition-colors ${
                          isSelected
                            ? 'bg-[#714B67] text-white'
                            : 'bg-[#EFE6ED] text-[#714B67] hover:bg-[#E2D2DE]'
                        }`}
                      >
                        {isSelected ? 'Configuring' : 'Configure'}
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Right: Configuration Drawer / Terms Panel (5 cols) */}
          <div className="lg:col-span-5 xl:col-span-4 bg-[#FBF9FA] p-5 overflow-y-auto flex flex-col gap-4 border-t lg:border-t-0 border-[#DEE2E6]">
            {selectedProduct ? (
              <div className="flex flex-col gap-4">
                <div className="pb-3 border-b border-[#DEE2E6]">
                  <span className="text-[10px] uppercase font-bold text-[#714B67] tracking-wider">
                    Configuration &amp; Pricing
                  </span>
                  <h3 className="text-sm font-extrabold text-[#212529] mt-0.5">{selectedProduct.name}</h3>
                  <div className="flex items-center gap-2 mt-1">
                    <span className="font-mono text-xs font-bold text-[#6C757D]">{selectedProduct.code}</span>
                    <span className="text-xs text-[#6C757D]">•</span>
                    <span className="text-xs text-[#6C757D]">{selectedProduct.category}</span>
                  </div>
                </div>

                {/* Variant Selector */}
                {loadingDetail ? (
                  <div className="py-4 text-center text-xs text-[#6C757D]">Loading product variants…</div>
                ) : productDetail?.variants && productDetail.variants.length > 0 ? (
                  <div className="flex flex-col gap-1.5">
                    <label className="text-xs font-bold text-[#212529] flex items-center justify-between">
                      <span>Select Hardware / Spec Variant</span>
                      <span className="text-[10px] text-[#6C757D] font-normal">
                        ({productDetail.variants.length} available)
                      </span>
                    </label>
                    <select
                      value={selectedVariant?.id || ''}
                      onChange={(e) => {
                        const v = productDetail.variants.find((item) => item.id === e.target.value);
                        setSelectedVariant(v || null);
                      }}
                      className="w-full px-3 py-2 text-xs font-semibold rounded-xl border border-[#DEE2E6] bg-white text-[#212529] focus:outline-none focus:ring-2 focus:ring-[#714B67]/20"
                    >
                      {productDetail.variants.map((v) => (
                        <option key={v.id} value={v.id}>
                          {v.sku} — {v.name} ({formatINR(v.selling_price)})
                        </option>
                      ))}
                    </select>

                    {selectedVariant && (
                      <div className="p-2.5 rounded-xl bg-white border border-[#DEE2E6] text-[11px] flex flex-col gap-1 mt-1">
                        <div className="flex justify-between">
                          <span className="text-[#6C757D]">Variant Stock:</span>
                          <span className="font-bold text-emerald-700">
                            {selectedVariant.total_free || 0} Free Units
                          </span>
                        </div>
                        {selectedVariant.attributes && Object.keys(selectedVariant.attributes).length > 0 && (
                          <div className="pt-1 border-t border-[#F1F1F1] flex flex-wrap gap-1">
                            {Object.entries(selectedVariant.attributes).map(([k, val]) => (
                              <span
                                key={k}
                                className="bg-[#F1F3F5] text-[#495057] px-2 py-0.5 rounded text-[10px] font-semibold"
                              >
                                {k}: {val}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                ) : null}

                {/* Quantity & Discount Form */}
                <div className="grid grid-cols-2 gap-3">
                  <div className="flex flex-col gap-1">
                    <label className="text-xs font-bold text-[#212529]">Quantity</label>
                    <div className="flex items-center rounded-xl border border-[#DEE2E6] bg-white overflow-hidden">
                      <button
                        type="button"
                        onClick={() => setQty((q) => Math.max(1, q - 1))}
                        className="px-3 py-2 text-xs font-bold text-[#212529] hover:bg-[#F1F1F1] transition-colors"
                      >
                        -
                      </button>
                      <input
                        type="number"
                        min="1"
                        value={qty}
                        onChange={(e) => setQty(Math.max(1, parseInt(e.target.value) || 1))}
                        className="w-full text-center font-mono font-bold text-xs outline-none py-2"
                      />
                      <button
                        type="button"
                        onClick={() => setQty((q) => q + 1)}
                        className="px-3 py-2 text-xs font-bold text-[#212529] hover:bg-[#F1F1F1] transition-colors"
                      >
                        +
                      </button>
                    </div>
                  </div>

                  <div className="flex flex-col gap-1">
                    <label className="text-xs font-bold text-[#212529]">Discount %</label>
                    <div className="flex items-center rounded-xl border border-[#DEE2E6] bg-white px-3 py-1.5">
                      <input
                        type="number"
                        min="0"
                        max="100"
                        value={discountPercent}
                        onChange={(e) =>
                          setDiscountPercent(Math.min(100, Math.max(0, parseFloat(e.target.value) || 0)))
                        }
                        className="w-full font-mono font-bold text-xs outline-none"
                      />
                      <span className="text-xs text-[#6C757D] font-bold">%</span>
                    </div>
                  </div>
                </div>

                {/* High Discount Warning */}
                {isHardwareHighDiscount && (
                  <div className="p-3 rounded-xl bg-amber-50 border border-amber-200 text-[11px] text-amber-900 flex items-start gap-2">
                    <span className="material-symbols-outlined text-[16px] text-amber-700 shrink-0">
                      warning
                    </span>
                    <div>
                      <strong className="font-bold">Discount Ceiling Triggered:</strong> Discount exceeds 15% hardware
                      limit. This quotation will require Sales Manager approval.
                    </div>
                  </div>
                )}

                {/* Financial Summary Card */}
                <div className="p-4 rounded-xl bg-white border border-[#DEE2E6] shadow-sm flex flex-col gap-2.5 text-xs">
                  <div className="flex justify-between text-[#6C757D]">
                    <span>Unit List Price</span>
                    <span className="font-mono font-bold text-[#212529]">{formatINR(currentUnitPrice)}</span>
                  </div>
                  <div className="flex justify-between text-[#6C757D]">
                    <span>Gross Subtotal ({qty} units)</span>
                    <span className="font-mono font-bold text-[#212529]">{formatINR(lineSubtotal)}</span>
                  </div>
                  {Number(discountPercent) > 0 && (
                    <div className="flex justify-between text-rose-700 font-semibold">
                      <span>Discount ({discountPercent}%)</span>
                      <span className="font-mono font-bold">-{formatINR(lineDiscountAmount)}</span>
                    </div>
                  )}
                  <div className="pt-2 border-t border-[#DEE2E6] flex justify-between items-baseline">
                    <span className="text-xs font-bold text-[#212529]">Net Line Total</span>
                    <span className="text-base font-extrabold text-[#714B67] font-mono">
                      {formatINR(lineNetTotal)}
                    </span>
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex flex-col gap-2 pt-2">
                  <button
                    onClick={handleAddCurrentLine}
                    disabled={adding}
                    className="w-full py-2.5 rounded-xl bg-[#714B67] hover:bg-[#5C3D54] disabled:opacity-60 text-white text-xs font-bold shadow-md transition-colors flex items-center justify-center gap-1.5"
                  >
                    <span className="material-symbols-outlined text-[18px]">add_shopping_cart</span>
                    {adding ? 'Adding to Quotation…' : 'Add to Quotation'}
                  </button>
                  <button
                    onClick={() => {
                      setSelectedProduct(null);
                      setSelectedVariant(null);
                      setProductDetail(null);
                    }}
                    className="w-full py-2 rounded-xl border border-[#DEE2E6] text-[#6C757D] text-xs font-bold hover:bg-white transition-colors"
                  >
                    Keep Browsing
                  </button>
                </div>
              </div>
            ) : (
              <div className="py-20 text-center text-xs text-[#6C757D] flex flex-col items-center gap-3">
                <div className="w-12 h-12 rounded-full bg-[#EFE6ED] text-[#714B67] flex items-center justify-center">
                  <span className="material-symbols-outlined text-[24px]">touch_app</span>
                </div>
                <div>
                  <p className="font-bold text-[#212529]">Select a Product to Configure</p>
                  <p className="text-[11px] text-[#6C757D] mt-1 max-w-[220px]">
                    Choose an item from the catalog on the left to set quantity, discount, and select specific variants.
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-[#DEE2E6] bg-[#FBF9FA] flex items-center justify-between text-xs text-[#6C757D]">
          <span>Tip: You can use "+ Quick Add" on any item to rapidly insert lines at standard pricing.</span>
          <button
            onClick={onClose}
            className="px-4 py-1.5 rounded-xl border border-[#DEE2E6] bg-white hover:bg-[#F1F1F1] text-[#212529] font-bold transition-colors"
          >
            Done
          </button>
        </div>

      </div>
    </div>
  );
}
