import { TextField, InputAdornment, IconButton } from "@mui/material";
import { FaSearch, FaTimes } from "react-icons/fa";

export default function SearchBar({
  value,
  onChange,
  placeholder = "Search...",
  width = "100%",
}) {
  const clearSearch = () => {
    if (onChange) {
      onChange({
        target: {
          value: "",
        },
      });
    }
  };

  return (
    <div style={{ width }}>
      <TextField
        fullWidth
        variant="outlined"
        size="small"
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <FaSearch className="text-gray-500" />
            </InputAdornment>
          ),

          endAdornment:
            value && value.length > 0 ? (
              <InputAdornment position="end">
                <IconButton size="small" onClick={clearSearch}>
                  <FaTimes className="text-gray-500" />
                </IconButton>
              </InputAdornment>
            ) : null,
        }}
        sx={{
          backgroundColor: "#fff",
          borderRadius: "12px",

          "& .MuiOutlinedInput-root": {
            borderRadius: "12px",
          },
        }}
      />
    </div>
  );
}
