import { TextField, Button, Grid, Container } from '@mui/material';

const AddTodo = ({ addTodo }) => {
  const handleAdd = (e) => {
    e.preventDefault();
    const name = e.target.elements.todoName.value;
    const dueDate = e.target.elements.dueDate.value;
    // Add the current date as the registeredDate
    const registeredDate = new Date().toISOString().split("T")[0];
    addTodo(name, registeredDate, dueDate);
  };

  return (
    <Container sx={{ marginY: 4 }}> {/* Add marginY to ensure a proper spacing from the table below */}
      <form onSubmit={handleAdd}>
        <Grid container spacing={2} justifyContent="center" alignItems="center">
          <Grid item>
            <TextField name="todoName" placeholder="TODO Name" required />
          </Grid>
          <Grid item>
            <TextField name="dueDate" type="date" required />
          </Grid>
          <Grid item>
            <Button type="submit" variant="contained">Add</Button>
          </Grid>
        </Grid>
      </form>
    </Container>
  );
};

export default AddTodo;
