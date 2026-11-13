import { useState } from 'react'
import { ArrowDownUp, ChevronLeft, ChevronRight } from 'lucide-react'
import type { RawBass2Record } from '../../types/api'

interface DataTableProps {
  records: RawBass2Record[]
  pageSize?: number
}

type SortField = keyof RawBass2Record

export function DataTable({ records, pageSize = 15 }: DataTableProps) {
  const [currentPage, setCurrentPage] = useState(1)
  const [sortField, setSortField] = useState<SortField>('Test #')
  const [sortAsc, setSortAsc] = useState(true)

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortAsc(!sortAsc)
    } else {
      setSortField(field)
      setSortAsc(true)
    }
  }

  const sortedRecords = [...records].sort((a, b) => {
    const valA = String(a[sortField] || '').trim()
    const valB = String(b[sortField] || '').trim()
    const numA = parseFloat(valA)
    const numB = parseFloat(valB)
    if (!isNaN(numA) && !isNaN(numB)) {
      return sortAsc ? numA - numB : numB - numA
    }
    return sortAsc ? valA.localeCompare(valB) : valB.localeCompare(valA)
  })

  const totalPages = Math.ceil(sortedRecords.length / pageSize) || 1
  const paginated = sortedRecords.slice((currentPage - 1) * pageSize, currentPage * pageSize)

  const renderCell = (value: string | undefined) => {
    if (value === undefined || value === null || value.trim() === '') {
      return <span className="cell-unavailable">blank</span>
    }
    if (value.trim().toLowerCase() === 'none') {
      return <span className="cell-unavailable">none</span>
    }
    return <span>{value}</span>
  }

  return (
    <div>
      <div className="editorial-table-wrap">
        <table className="editorial-table">
          <thead>
            <tr>
              <th onClick={() => handleSort('PI')} style={{ cursor: 'pointer' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <span>PI</span>
                  <ArrowDownUp size={11} />
                </div>
              </th>
              <th onClick={() => handleSort('Test #')} style={{ cursor: 'pointer' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <span>Test #</span>
                  <ArrowDownUp size={11} />
                </div>
              </th>
              <th>Fuel Sample Material</th>
              <th onClick={() => handleSort('Calibrated  initial O2 % by vol ')} style={{ cursor: 'pointer' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <span>Initial O₂ (% vol)</span>
                  <ArrowDownUp size={11} />
                </div>
              </th>
              <th onClick={() => handleSort('Calibrated final O2 % by vol')} style={{ cursor: 'pointer' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <span>Final O₂ (% vol)</span>
                  <ArrowDownUp size={11} />
                </div>
              </th>
              <th>Flow Restrictor</th>
              <th>Fan Display</th>
              <th>Air Display</th>
              <th>Total Frames Shot</th>
              <th>Initial CO₂ (%)</th>
              <th>Final CO₂ (%)</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {paginated.map((r, i) => (
              <tr key={`${r.PI}-${r['Test #']}-${i}`}>
                <td className="cell-mono" style={{ fontWeight: 600 }}>{renderCell(r.PI)}</td>
                <td className="cell-mono" style={{ color: '#D96C32', fontWeight: 600 }}>{renderCell(r['Test #'])}</td>
                <td style={{ maxWidth: '240px', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {renderCell(r['Fuel Sample Material'])}
                </td>
                <td className="cell-mono">{renderCell(r['Calibrated  initial O2 % by vol '])}</td>
                <td className="cell-mono">{renderCell(r['Calibrated final O2 % by vol'])}</td>
                <td className="cell-mono">{renderCell(r['Flow restrictor'])}</td>
                <td className="cell-mono">{renderCell(r['Fan display'])}</td>
                <td className="cell-mono">{renderCell(r['Air display'])}</td>
                <td className="cell-mono">{renderCell(r['Total Frames Shot'])}</td>
                <td className="cell-mono">{renderCell(r['Initial CO2 % by vol'])}</td>
                <td className="cell-mono">{renderCell(r['Final CO2 % by vol'])}</td>
                <td className="cell-mono">{renderCell(r.Date)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: '14px', fontSize: '11px', color: '#686861', fontFamily: 'monospace' }}>
        <span>
          Showing {(currentPage - 1) * pageSize + 1} - {Math.min(currentPage * pageSize, sortedRecords.length)} of {sortedRecords.length} records
        </span>
        <div style={{ display: 'flex', gap: '8px' }}>
          <button
            className="btn btn-secondary btn-sm"
            disabled={currentPage <= 1}
            onClick={() => setCurrentPage((p) => Math.max(p - 1, 1))}
          >
            <ChevronLeft size={13} />
            <span>Previous</span>
          </button>
          <span style={{ display: 'flex', alignItems: 'center', padding: '0 8px' }}>
            Page {currentPage} of {totalPages}
          </span>
          <button
            className="btn btn-secondary btn-sm"
            disabled={currentPage >= totalPages}
            onClick={() => setCurrentPage((p) => Math.min(p + 1, totalPages))}
          >
            <span>Next</span>
            <ChevronRight size={13} />
          </button>
        </div>
      </div>
    </div>
  )
}
