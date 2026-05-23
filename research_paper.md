# Product Optimization & Revenue Contribution Analysis
## Afficionado Coffee Roasters — Research Paper (2025)

**Scope:** 149,116 Transactions · 3 Stores · 80 Products · 9 Categories
**Total Revenue:** $698,812.33 · **Stores:** Lower Manhattan, Hell's Kitchen, Astoria (NYC)

---

## 1. Abstract
This paper presents a comprehensive product-level revenue analysis for Afficionado Coffee Roasters. Coffee and Tea together contribute 66.7% of total revenue. A Pareto concentration means 42 products account for 80% of all revenue. Drinking Chocolate leads on per-SKU efficiency ($18,104/SKU) while Loose Tea ($1,402/SKU) is the primary rationalisation target. Five strategic recommendations are provided to improve menu efficiency and profitability.

---

## 2. Dataset & Validation
- **149,116 records**, no null values in key fields
- Derived field: `revenue = transaction_qty × unit_price`
- Price range: $1.75–$45.00 per unit
- 80 unique products, 29 product types, 9 categories, 3 stores

---

## 3. EDA Summary

### Peak Hours
| Hour | Transactions |
|------|-------------|
| 10:00 | 18,545 (peak) |
| 09:00 | 17,764 |
| 08:00 | 17,654 |

### Store Distribution
| Store | Transactions | Revenue |
|-------|-------------|---------|
| Hell's Kitchen | 50,735 | $236,511 |
| Astoria | 50,599 | $232,244 |
| Lower Manhattan | 47,782 | $230,057 |

---

## 4. Product Performance

### Top 10 by Revenue
| Rank | Product | Category | Revenue | Rev % |
|------|---------|----------|---------|-------|
| 1 | Sustainably Grown Organic Lg | Drinking Chocolate | $21,152 | 3.03% |
| 2 | Dark Chocolate Lg | Drinking Chocolate | $21,006 | 3.01% |
| 3 | Latte Rg | Coffee | $19,112 | 2.73% |
| 4 | Cappuccino Lg | Coffee | $17,642 | 2.52% |
| 5 | Morning Sunrise Chai Lg | Tea | $17,384 | 2.49% |
| 6 | Latte | Coffee | $17,258 | 2.47% |
| 7 | Jamaican Coffee River Lg | Coffee | $16,481 | 2.36% |
| 8 | Sustainably Grown Organic Rg | Drinking Chocolate | $16,234 | 2.32% |
| 9 | Cappuccino | Coffee | $15,998 | 2.29% |
| 10 | Brazilian Lg | Coffee | $15,110 | 2.16% |

### Bottom 5 by Revenue
| Rank | Product | Category | Revenue | Rev % |
|------|---------|----------|---------|-------|
| 76 | Guatemalan Sustainably Grown | Coffee beans | $1,340 | 0.19% |
| 77 | Spicy Eye Opener Chai | Loose Tea | $1,336 | 0.19% |
| 78 | Earl Grey | Loose Tea | $1,271 | 0.18% |
| 79 | Lemon Grass | Loose Tea | $1,360 | 0.19% |
| 80 | Dark Chocolate (packaged) | Packaged Chocolate | $755 | 0.11% |

---

## 5. Category Analysis
| Category | Revenue | Rev % | SKUs | Rev/SKU |
|----------|---------|-------|------|---------|
| Coffee | $269,952 | 38.6% | 21 | $12,855 |
| Tea | $196,406 | 28.1% | 16 | $12,275 |
| Bakery | $82,316 | 11.8% | 11 | $7,483 |
| Drinking Chocolate | $72,416 | 10.4% | 4 | **$18,104** |
| Coffee beans | $40,085 | 5.7% | 10 | $4,009 |
| Branded | $13,607 | 1.9% | 3 | $4,536 |
| Loose Tea | $11,214 | 1.6% | 8 | **$1,402** |
| Flavours | $8,409 | 1.2% | 4 | $2,102 |
| Packaged Chocolate | $4,408 | 0.6% | 3 | $1,469 |

---

## 6. Pareto Analysis
- **42 of 80 products (52.5%)** → **80% of revenue**
- Top 10 products → **25.4%** of total revenue
- Bottom 38 products → only **20%** of revenue (47.5% of SKUs)

---

## 7. Strategic Recommendations

| Priority | Action | Impact |
|----------|--------|--------|
| 🔴 High | Rationalise Loose Tea: 8 → 3 SKUs | Reduce complexity, recover staff time |
| 🔴 High | Promote Drinking Chocolate as hero category | +2–4% revenue from high-margin products |
| 🟡 Medium | Run 90-day simplified menu trial (remove bottom 15 SKUs) | Faster service, lower training cost |
| 🟡 Medium | Reduce Coffee Beans: 10 → 5 premium SKUs | Better retail positioning |
| 🟢 Low | Standardise menu across all 3 stores | Unified ops, faster rollouts |

**Estimated incremental revenue from recommendations: +$35,000–$56,000/year**

---

## 8. Post-Optimisation KPI Targets
| KPI | Current | Target |
|-----|---------|--------|
| Active SKUs | 80 | 55–60 |
| Products for 80% revenue | 42 | 35 |
| Loose Tea SKUs | 8 | 3 |
| Drinking Choc Rev % | 10.4% | 13–15% |
| Portfolio Avg Rev/SKU | $8,735 | $11,000+ |

---
*Analysis: Python (pandas, plotly) · Dashboard: Streamlit*
