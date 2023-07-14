import { useState } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Pagination } from '@mui/material';

const PAGE_SIZE = 5;

const TodoList = ({ todos, selectTodo, selectedTodoId }) => {
  const [page, setPage] = useState(1);

  const displayedTodos = todos.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);

  return (
    <TableContainer component={Paper} sx={{ backgroundColor: 'white' }}> {/* Change background color to white */}
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Name</TableCell>
            <TableCell>Registered Date</TableCell>
            <TableCell>Due Date</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {displayedTodos.map((todo, index) => (
            <TableRow
              key={todo.id}
              onClick={() => selectTodo(todo.id)}
              sx={{ '&.Mui-selected': { backgroundColor: "lightblue" } }}
              selected={todo.id === selectedTodoId}
            >
              <TableCell>{todo.name}</TableCell>
              <TableCell>{todo.registeredDate}</TableCell>
              <TableCell>{todo.dueDate}</TableCell>
            </TableRow>
          ))}
          {/* Add an empty row if there are not enough todos */}
          {[...Array(PAGE_SIZE - displayedTodos.length)].map((_, index) => (
            <TableRow key={index}>
              <TableCell />
              <TableCell />
              <TableCell />
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <Pagination count={Math.ceil(todos.length / PAGE_SIZE)} page={page} onChange={(_, value) => setPage(value)} />
    </TableContainer>
  );
};

export default TodoList;
