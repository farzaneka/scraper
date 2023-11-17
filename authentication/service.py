import json

from nameko.rpc import rpc
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from authentication.auth import generate_access_token, verify_token
from authentication.database import SessionLocal
from authentication.models import Member


class AuthenticationService:
    name = 'authentication'
    session = SessionLocal()

    @rpc
    def register_member(self, request):
        email = request.get('email')
        username = request.get('username')
        password = request.get('password')
        password_hash = generate_password_hash(password)

        try:
            member = Member(
                username=username,
                email=email,
                password=password_hash,
            )
            self.session.add(member)
            self.session.commit()
            self.session.close()

        except IntegrityError:
            raise Exception("Password or username already exists")

        return json.dumps(
            {
                "member": {"username": username, "email": email},
                "status_code": 201
            }
        )

    @rpc
    def login_member(self, request):
        email = request.get('email')
        username = request.get('username')
        password = request.get('password')
        member = self.session.query(Member) \
            .filter(Member.email == email) \
            .one_or_none()

        if member is not None:
            is_pass_correct = check_password_hash(member.password, password)
            if is_pass_correct:
                access_token = generate_access_token(
                    member.id,
                    username,
                    email,
                )

                return json.dumps({
                    'member': {
                        'access_token': access_token,
                        'username': member.username,
                        'email': member.email
                    },
                    "status_code": 200
                })

        return json.dumps({"error": "Wrong credentials", "status_code": 400})

    @rpc
    def get_member(self, member_id):
        member_id = self.session.query(Member.id) \
            .filter(Member.id == member_id) \
            .scalar()
        self.session.close()
        if member_id is not None:
            return member_id

    @rpc
    def verify_token(self, request):
        token = request.headers.get('Authorization')
        if verify_token(token) is not True:
            raise Exception("Token is expired")

