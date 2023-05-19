from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict

from flask import Flask, request, make_response


app = Flask(__name__, static_folder='.', static_url_path='')


class InvalidArgument(Exception):
    pass


class UnexpectedArgument(Exception):
    pass


def get_incrementer():
    count = 0
    
    def inner():
        nonlocal count
        count += 1
        return count
    
    return inner


@dataclass(frozen=True)
class Todo:
    id: str
    content: str
    deadline: datetime
    is_finished: bool = field(default=False)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def finish(self):
        self.is_finished = True
        self.updated_at = datetime.now()

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, **kwargs):
        if 'content' not in kwargs:
            raise InvalidArgument('field content is required')
        content = kwargs['content']
        if not isinstance(content, str):
            raise TypeError('field content should be string')
        
        if 'deadline' not in kwargs:
            raise InvalidArgument('field deadline is required')
        s_deadline = kwargs['deadline']
        if not isinstance(s_deadline, str):
            raise TypeError('field deadline should be string-compatible')
        deadline = datetime.strptime(s_deadline, '%Y-%m-%d')
        
        if len(kwargs) != 2:
            raise UnexpectedArgument('fields must include only content & deadline')
        return cls(
            incrementer(),
            content,
            deadline,
            )


data: Dict[int, Todo] = {}
incrementer = get_incrementer()


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/1.0/todos', methods=['GET', 'POST'])
def todos():
    if request.method == 'GET':
        items = []
        for _, d in sorted(data.items(), key=lambda x: x[0]):
            if d.is_finished:
                continue
            items.append(d.to_dict())
        
        res = {
            'items': items,
            'total': len(data),
        }
        return make_response(res, 200)
    if request.method == 'POST':
        try:
            d = Todo.from_dict(**request.get_json())
        except Exception as e:
            return make_response(str(e), 500)
        data[d.id] = d
        return make_response(d.to_dict(), 200)
    return make_response('Method Not Allowed', 405)


@app.route('/api/1.0/todos/<todo_id>')
def todo(todo_id: str):
    if not todo_id.isdigit():
        return make_response('Invalid Argument: id should be integer compatible', 500)
    if int(todo_id) not in data:
        return make_response('Not Found', 404)
    if request.method == 'GET':
        return make_response(data[int(todo_id)].to_dict(), 200)
    return make_response('Method Not Allowed', 405)


app.run(port=8080, debug=True)
