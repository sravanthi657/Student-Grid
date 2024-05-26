import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './StudentGrid.css';

const fetchStudents = async (queryParams) => {
  try {
    const response = await axios.get(`${process.env.REACT_APP_API_BASE_URL}/api/students/`, {
      params: queryParams,
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching students:', error);
    throw error;
  }
};

const StudentGrid = () => {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    name: '',
    total_marks_min: '',
    total_marks_max: '',
  });
  const [pagination, setPagination] = useState({
    page: 1,
    page_size: 10,
    total: 0,
  });

  useEffect(() => {
    const fetchStudentsData = async () => {
      setLoading(true);
      try {
        const queryParams = {
          page: pagination.page,
          page_size: pagination.page_size,
          ...filters,
        };
        const studentsData = await fetchStudents(queryParams);
        setStudents(studentsData.results);
        setPagination({
          ...pagination,
          total: studentsData.count,
        });
      } catch (error) {
        setError('Failed to fetch students. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchStudentsData();
  }, [filters, pagination.page, pagination.page_size]);

  const handleFilterChange = (event) => {
    const { name, value } = event.target;
    setFilters((prevFilters) => ({
      ...prevFilters,
      [name]: value,
    }));
    // Reset pagination to page 1 when filters change
    setPagination({ ...pagination, page: 1 });
  };

  const handlePageChange = (newPage) => {
    setPagination((prevPagination) => ({
      ...prevPagination,
      page: newPage,
    }));
  };

  // Calculate total pages
  const totalPages = Math.ceil(pagination.total / pagination.page_size);

  return (
    <div className="container">
      <h1 className="title">Student Grid</h1>
      <form className="filter-form">
        <div className="filter-group">
          <label htmlFor="name">Name:</label>
          <input
            type="text"
            id="name"
            name="name"
            value={filters.name}
            onChange={handleFilterChange}
          />
        </div>
        <div className="filter-group">
          <label htmlFor="total_marks_min">Total Marks Min:</label>
          <input
            type="number"
            id="total_marks_min"
            name="total_marks_min"
            value={filters.total_marks_min}
            onChange={handleFilterChange}
          />
        </div>
        <div className="filter-group">
          <label htmlFor="total_marks_max">Total Marks Max:</label>
          <input
            type="number"
            id="total_marks_max"
            name="total_marks_max"
            value={filters.total_marks_max}
            onChange={handleFilterChange}
          />
        </div>
      </form>
      {loading ? (
        <p className="loading">Loading...</p>
      ) : error ? (
        <p className="error">{error}</p>
      ) : students.length === 0 ? (
        <p>No students found.</p>
      ) : (
        <>
          <table className="student-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Total Marks</th>
              </tr>
            </thead>
            <tbody>
              {students.map((student) => (
                <tr key={student.id}>
                  <td>{student.id}</td>
                  <td>{student.name}</td>
                  <td>{student.total_marks}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="pagination">
            <button
              onClick={() => handlePageChange(pagination.page - 1)}
              disabled={pagination.page === 1}
            >
              <span className="icon">&lt;</span>
            </button>
            <span>{pagination.page}</span>
            <button
              onClick={() => handlePageChange(pagination.page + 1)}
              disabled={pagination.page === totalPages}
            >
              <span className="icon">&gt;</span>
            </button>
            <span>of {totalPages}</span>
          </div>
        </>
      )}
    </div>
  );
};

export default StudentGrid;
