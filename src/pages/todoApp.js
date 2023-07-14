import { useState } from 'react';
import useLocalStorage from '../hooks/localStorage';
import TodoList from '../components/todoList';
import AddTodo from '../components/addTodo';
import TodoDetail from '../components/todoDetail';

const TodoApp = () => {
  const [todos, setTodos] = useLocalStorage('todos', []);
  const [selectedTodoId, setSelectedTodoId] = useState(null);

  const addTodo = (name, registeredDate, dueDate) => {
    const newTodo = {
      id: Math.random(),
      name,
      registeredDate,
      dueDate
    };
    setTodos([...todos, newTodo]);
  };

  const selectTodo = (id) => {
    setSelectedTodoId(id);
  };

  const updateTodo = (id, newName, newDueDate) => {
    const updatedTodos = todos.map((todo) =>
      todo.id === id ? { ...todo, name: newName, dueDate: newDueDate } : todo
    );
    setTodos(updatedTodos);
  };

  const closeTodoDetail = () => {
    setSelectedTodoId(null);
  }

  const selectedTodo = todos.find((todo) => todo.id === selectedTodoId);

  return (
    <div>
      <AddTodo addTodo={addTodo} />
      <TodoList todos={todos} selectTodo={selectTodo} selectedTodoId={selectedTodoId} />
      {selectedTodo && <TodoDetail todo={selectedTodo} updateTodo={updateTodo} onClose={closeTodoDetail} />}
    </div>
  );
};

export default TodoApp;
