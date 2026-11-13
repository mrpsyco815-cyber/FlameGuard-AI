import { type FormEvent, useState } from 'react'
import { ArrowRight, Search } from 'lucide-react'

interface SearchInputProps {
  value: string
  onChange: (val: string) => void
  onSubmit?: () => void
  placeholder?: string
  buttonText?: string
  isLoading?: boolean
}

export function SearchInput({
  value,
  onChange,
  onSubmit,
  placeholder = 'Enter research query...',
  buttonText = 'Search Evidence',
  isLoading = false,
}: SearchInputProps) {
  const [internalValue, setInternalValue] = useState(value)

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    onChange(internalValue)
    if (onSubmit) onSubmit()
  }

  return (
    <form className="search-input-group" onSubmit={handleSubmit}>
      <div className="search-field">
        <Search size={18} style={{ color: '#686861', flexShrink: 0 }} />
        <input
          type="text"
          value={internalValue}
          onChange={(e) => {
            setInternalValue(e.target.value)
            onChange(e.target.value)
          }}
          placeholder={placeholder}
          aria-label="Scientific search input"
        />
      </div>
      <button
        type="submit"
        className="btn btn-primary"
        disabled={isLoading || internalValue.trim().length < 2}
        style={{ minWidth: '140px' }}
      >
        {isLoading ? (
          <span>Searching...</span>
        ) : (
          <>
            <span>{buttonText}</span>
            <ArrowRight size={14} />
          </>
        )}
      </button>
    </form>
  )
}
