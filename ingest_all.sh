#!/usr/bin/env bash
# =============================================================================
# ingest_all.sh — Ingest all datasets into the AI Cyber Strategy Analyst API
#
# Chunk sizes are tuned per-document based on structure analysis:
#   ISO 27001   → 800  / 100   (dense normative clauses + Annex A controls)
#   NIST CSF    → 1200 / 150   (clean numbered sections, prose-heavy)
#   CIS Controls→ 1200 / 200   (Control blocks + subsections + safeguard tables)
#   GDPR        → 1000 / 150   (topic-heading prose briefing)
#   JSON datasets → 0/0        (each item = one chunk, preset not used)
#
# Usage:
#   chmod +x ingest_all.sh
#   ./ingest_all.sh [API_BASE_URL]
#   Default API_BASE_URL = http://localhost:8000
# =============================================================================

set -euo pipefail

BASE="${1:-http://localhost:8000}"
DATA_DIR="$(cd "$(dirname "$0")/data" && pwd)"
PASS=0
FAIL=0
SKIP=0

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_ok()   { echo -e "${GREEN}[OK]${NC}    $1"; }
log_err()  { echo -e "${RED}[FAIL]${NC}  $1"; }
log_skip() { echo -e "${YELLOW}[SKIP]${NC}  $1"; }
log_info() { echo -e "${BLUE}[INFO]${NC}  $1"; }

# -----------------------------------------------------------------------------
# Health check
# -----------------------------------------------------------------------------
echo ""
log_info "Checking API health at $BASE ..."
if ! curl -sf "$BASE/" > /dev/null; then
  echo -e "${RED}ERROR: API is not reachable at $BASE${NC}"
  echo "       Start it with: uvicorn app.main:app --reload"
  exit 1
fi
log_ok "API is up"
echo ""

# -----------------------------------------------------------------------------
# Helper: upload a PDF/DOCX/TXT file
# -----------------------------------------------------------------------------
upload_file() {
  local filepath="$1"
  local category="$2"
  local source_name="$3"
  local chunk_size="$4"
  local chunk_overlap="$5"
  local filename
  filename="$(basename "$filepath")"

  if [ ! -f "$filepath" ]; then
    log_skip "$filename — file not found"
    ((SKIP++)) || true
    return
  fi

  local filesize
  filesize=$(wc -c < "$filepath")
  if [ "$filesize" -eq 0 ]; then
    log_skip "$filename — empty file"
    ((SKIP++)) || true
    return
  fi

  log_info "Uploading $filename (chunk=$chunk_size, overlap=$chunk_overlap) ..."
  local response http_code body
  response=$(curl -sf -w "\n%{http_code}" \
    -X POST "$BASE/documents/upload" \
    -F "file=@$filepath" \
    -F "category=$category" \
    -F "source_name=$source_name" \
    -F "chunk_size=$chunk_size" \
    -F "chunk_overlap=$chunk_overlap" 2>&1) || true

  http_code=$(echo "$response" | tail -n1)
  body=$(echo "$response" | head -n-1)

  if [[ "$http_code" == "200" ]]; then
    local chunks
    chunks=$(echo "$body" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('document',{}).get('chunk_count','?'))" 2>/dev/null || echo "?")
    log_ok "$filename → $chunks chunks  [category=$category]"
    ((PASS++)) || true
  else
    log_err "$filename — HTTP $http_code: $body"
    ((FAIL++)) || true
  fi
}

# -----------------------------------------------------------------------------
# Helper: ingest a JSON dataset
# -----------------------------------------------------------------------------
ingest_json() {
  local filepath="$1"
  local category="$2"
  local source_name="$3"
  local filename
  filename="$(basename "$filepath")"

  if [ ! -f "$filepath" ]; then
    log_skip "$filename — file not found"
    ((SKIP++)) || true
    return
  fi

  local filesize
  filesize=$(wc -c < "$filepath")
  if [ "$filesize" -eq 0 ]; then
    log_skip "$filename — empty file (no data yet)"
    ((SKIP++)) || true
    return
  fi

  log_info "Ingesting $filename ..."
  local response http_code body
  response=$(curl -sf -w "\n%{http_code}" \
    -X POST "$BASE/documents/ingest-json" \
    -F "file=@$filepath" \
    -F "category=$category" \
    -F "source_name=$source_name" 2>&1) || true

  http_code=$(echo "$response" | tail -n1)
  body=$(echo "$response" | head -n-1)

  if [[ "$http_code" == "200" ]]; then
    local count
    count=$(echo "$body" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('document',{}).get('chunk_count','?'))" 2>/dev/null || echo "?")
    log_ok "$filename → $count items  [category=$category]"
    ((PASS++)) || true
  else
    log_err "$filename — HTTP $http_code: $body"
    ((FAIL++)) || true
  fi
}

# =============================================================================
# INGEST ALL DATA
# =============================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  PDF / DOCX — Framework Documents"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ISO 27001:2022 — dense normative standard with Annex A controls
# Small chunks (800) preserve individual clause/control meaning
upload_file \
  "$DATA_DIR/ISO_IEC-270012022-ed.3.pdf" \
  "iso" \
  "ISO/IEC 27001:2022" \
  800 \
  100

# NIST Cybersecurity Framework 2.0 — clean numbered sections, prose-heavy
# Larger chunks (1200) keep section context intact
upload_file \
  "$DATA_DIR/NIST.CSWP.29.pdf" \
  "nist" \
  "NIST CSF 2.0" \
  1200 \
  150

# CIS Controls v8.1 — Control blocks + safeguard tables
# Large chunks (1200) + high overlap (200) keep safeguard tables together
upload_file \
  "$DATA_DIR/CIS_Controls_Guide_v8.1.2_0325_v2.pdf" \
  "cis" \
  "CIS Controls v8.1" \
  1200 \
  200

# GDPR EPSU Briefing — topic-heading prose, short pages
# Medium chunks (1000) match page density
upload_file \
  "$DATA_DIR/GDPR_FINAL_EPSU.pdf" \
  "gdpr" \
  "GDPR EPSU Briefing" \
  1000 \
  150

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  JSON — Operational Datasets"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Audit findings — internal policy controls (15 items)
ingest_json \
  "$DATA_DIR/audit_finding_dataset.json" \
  "audit" \
  "Internal Audit Findings 2025"

# Risk register — enterprise risks with scores (25 items)
ingest_json \
  "$DATA_DIR/risk_register_dataset.json" \
  "risk" \
  "Enterprise Risk Register 2025"

# Cloud migration — workload security gaps (25 items)
ingest_json \
  "$DATA_DIR/cloud_migration_dataset.json" \
  "business" \
  "Cloud Migration Risk Assessment"

# Third-party risk — vendor compliance records (25 items)
ingest_json \
  "$DATA_DIR/third_party_risk_dataset.json" \
  "risk" \
  "Third-Party Risk Register 2025"

# Incident reports — skipped if empty
ingest_json \
  "$DATA_DIR/incident_reports_dataset.json" \
  "incident" \
  "Incident Reports"

# Business plan — skipped if empty
ingest_json \
  "$DATA_DIR/business_plan.json" \
  "business" \
  "Business Plan"

# =============================================================================
# SUMMARY
# =============================================================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "  ${GREEN}Passed: $PASS${NC}   ${RED}Failed: $FAIL${NC}   ${YELLOW}Skipped: $SKIP${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ "$FAIL" -gt 0 ]; then
  echo -e "${RED}Some ingestions failed. Check the errors above.${NC}"
  exit 1
fi

echo -e "${GREEN}All data ingested successfully.${NC}"
echo "  Verify at: $BASE/documents/items"
echo ""
