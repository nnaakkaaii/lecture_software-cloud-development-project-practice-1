import { Dialog, DialogTitle, DialogContent, TextField, DialogActions, Button } from '@mui/material';

const TodoDetail = ({ todo, updateTodo, onClose }) => {
  if (!todo) return null;
  const handleUpdate = (e) => {
    e.preventDefault();
    const updatedName = e.target.todoName.value;
    const updatedDueDate = e.target.dueDate.value;
    updateTodo(todo.id, updatedName, updatedDueDate);
  };

  return (
    <Dialog open={true} onClose={onClose}>
      <DialogTitle>Edit Todo</DialogTitle>
      <DialogContent>
        <form onSubmit={handleUpdate}>
          <TextField name="todoName" defaultValue={todo.name} />
          <TextField name="dueDate" type="date" defaultValue={todo.dueDate} />
          <DialogActions>
            <Button type="submit" variant="contained">Update</Button>
          </DialogActions>
        </form>
      </DialogContent>
    </Dialog>
  );
};

export default TodoDetail;
