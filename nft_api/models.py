import uuid
from datetime import datetime
from nft_api import app, db, ROW_PER_PAGE
from passlib.apps import custom_app_context as pwd_context
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import Serializer, BadSignature, SignatureExpired
from flask_login import UserMixin

# nft_trades = db.Table('nft_trades', db.Column('nft_id', db.Integer, db.ForeignKey('nft.id')), db.Column('trades_id', db.Integer, db.ForeignKey('trades.id')))
# NFT Many to Many field
# nfts = db.relationship('NFT', secondary=nft_trades, backref="trades")

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(128), index = True)
    password = db.Column(db.String(256))
    name = db.Column(db.String(128))
    image = db.Column(db.String(128))
    admin = db.Column(db.Boolean, default=False) 
    account = db.Column(db.String(128), unique=True)
    network_id = db.Column(db.Integer)
    nonce = db.Column(db.String(128))
    network_name = db.Column(db.String(64))
    avatar = db.Column(db.String(128))
    wallet_provider = db.Column(db.String(32))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_nonce(self, address):
        if address:
            obj = self.query.filter_by(account=address).first()
            if obj:
                return obj.nonce
        return ""

    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

    def row2dict(self, row):
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))
        return d
        
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user

    def create(self, name="", email="", password="", account="", admin=False):
        """Create a new user"""
        if admin:
            user = self.get_by_email(email)
            if user:
                return
            new_user = User(name=name, email=email, password=self.encrypt_password(password), admin=admin)
        else:
            user = self.get_by_email(email)
            if user:
                return
            new_user = User(name=name, email=account, account=account, password=password, admin=admin, nonce=uuid.uuid4().hex)

        db.session.add(new_user)
        db.session.commit()
        return self.get_by_id(new_user.id)


    def get_all(self):
        return self.queryset_to_list(self.query.all())

    def queryset_to_list(self, queryset):
        l = []
        for obj in queryset:
            l.append(self.row2dict(obj))
        return l

    def get_by_id(self, user_id):
        """Get a user by id"""
        user = self.query.filter_by(id=user_id).first()
        if not user:
            return
        user = self.row2dict(user)
        user.pop("password")
        return user

    def get_by_id_obj(self, id):
        """Get a user by id"""
        obj = self.query.filter_by(id=id).first()
        if not obj:
            return
        return obj

    def delete_one(self, id):
        del_obj = self.get_by_id_obj(id)
        db.session.delete(del_obj)
        db.session.commit()

    def get_by_email(self, email):
        """Get a user by user"""
        user = self.query.filter_by(account=email).first()
        if not user:
            return
        user = self.row2dict(user)
        return user

    def update_one(self, id, *args, **kwargs):
        get_obj = self.get_by_id_obj(id)
        for key, value in kwargs.items():
            setattr(get_obj, key, value)
        db.session.commit()

    def delete(self, user_id):
        """Delete a user"""
        Books().delete_by_user_id(user_id)
        user = db.users.delete_one({"_id": bson.ObjectId(user_id)})
        user = self.get_by_id(user_id)
        return user


    def encrypt_password(self, password):
        """Encrypt password"""
        return generate_password_hash(password)

    def login(self, email, password):
        """Login a user"""
        user = self.get_by_email(email)
        print(user)
        if user:
            if user["admin"] == "True":
                if not user or not check_password_hash(user["password"], password):
                    return
            else:
                if not user or user["password"] != password:
                    return
            user.pop("password")
        else:
            return
        return user

class NFT(db.Model):
    __tablename__ = 'nft'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128))
    address = db.Column(db.String(128))
    image = db.Column(db.String(128))
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def create(self, *args, **kwargs):
        new_nft = NFT(**kwargs)
        db.session.add(new_nft)
        db.session.commit()
        return self.get_by_id(new_nft.id)

    def serch(self, name):
        return self.quearyset_to_list(self.query.filter(NFT.name.like("%" + name + "%")).all())

    def get_all(self):
        return self.queryset_to_list(self.query.all())

    def user_get_all(self, owner_id):
        return self.queryset_to_list(self.query.filter_by(owner=owner_id).all())


    def queryset_to_list(self, queryset):
        l = []
        for obj in queryset:
            l.append(self.row2dict(obj))
        return l

    def row2dict(self, row):
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))
        return d
    
    def delete_one(self, id):
        del_obj = self.get_by_id_obj(id)
        db.session.delete(del_obj)
        db.session.commit()
    
    def update_one(self, id, *args, **kwargs):
        get_obj = self.get_by_id_obj(id)
        for key, value in kwargs.items():
            setattr(get_obj, key, value)
        db.session.commit()

    def get_by_id_obj(self, id):
        obj = self.query.filter_by(id=id).first()
        if not obj:
            return
        return obj

    def get_by_id(self, id):
        """Get a user by id"""
        obj = self.query.filter_by(id=id).first()
        if not obj:
            return
        obj = self.row2dict(obj)
        return obj

    def get_by_user_id(self, owner_id):
        """Get a user by id"""
        obj = self.query.filter_by(owner=owner_id).first()
        if not obj:
            return
        obj = self.row2dict(obj)
        return obj

class Trades(db.Model):
    __tablename__ = 'trades'
    id = db.Column(db.Integer, primary_key = True)
    status = db.Column(db.Boolean, default = False)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    client_address = db.Column(db.String(128))
    client_nft_address = db.Column(db.String(128))
    client_nft_name = db.Column(db.String(128))
    client_nft_token_id = db.Column(db.String(128))
    our_fake_address = db.Column(db.String(128))
    our_fake_name = db.Column(db.String(128))
    our_nft_token_id = db.Column(db.String(128))
    our_nft_name = db.Column(db.String(128)) 
    our_nft_address = db.Column(db.String(128))    
    our_address = db.Column(db.String(128))
    signed_maker_data = db.Column(db.Text)
    our_image_icon = db.Column(db.String(256))
    our_nft_image = db.Column(db.String(256))
    client_nft_image = db.Column(db.String(256))
    our_nft_icon = db.Column(db.String(256))
    client_nft_icon = db.Column(db.String(256))
    client_fake_nft_addr = db.Column(db.String(256))
    our_fake_nft_addr = db.Column(db.String(256))
    our_fake_token_id = db.Column(db.String(256))
    client_fake_token_id = db.Column(db.String(256))
    eth_total = db.Column(db.Float, default=0)

    def create(self, *args, **kwargs):
        new_trades = Trades(**kwargs)
        db.session.add(new_trades)
        db.session.commit()
        _nfts = kwargs.get("nfts")
        if _nfts:
            if isinstance(_nfts, list):
                for nft in _nfts:
                    self.add_nft(new_trades, nft)

        
        return self.get_by_id(new_trades.id)

    def search(self, unique_string):
        return self.queryset_to_list(self.query.filter(Trades.unique_string.like("%" + unique_string + "%")).all())

    def add_nft(self, trade, nft_id):
        nft = NFT.query.filter_by(id=nft_id).first()
        if not nft:
            return
        if nft not in trade.nfts: 
            trade.nfts.append(nft)
        
        db.session.commit()
        return self.get_by_id(self.id)
    
    def get_trade_nfts(self, trade_id):
        trade = self.get_by_id_obj(trade_id)
        return self.get_all_from_queryset(trade.nfts) 
        
    def get_all(self):
        # .order_by(self.created_at.desc())
        return self.queryset_to_list(self.query.all())

    def get_all_from_queryset(self, queryset):
        return self.queryset_to_list(queryset)

    def get_client_trades(self, client_address):
        # , status=False
        return self.queryset_to_list(self.query.filter_by(client_address=client_address).all())

    def user_get_all(self, owner_id):
        return self.queryset_to_list(self.query.filter_by(owner=owner_id).all())


    def queryset_to_list(self, queryset):
        l = []
        for obj in queryset:
            l.append(self.row2dict(obj))
        return l

    def row2dict(self, row):
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))
        return d
    
    def delete_one(self, id):
        del_obj = self.get_by_id_obj(id)
        db.session.delete(del_obj)
        db.session.commit()
    
    def update_one(self, id, *args, **kwargs):
        if kwargs.get("status"):
            if kwargs["status"] == "True" or kwargs["status"] == "true" :
                kwargs["status"] = True
            else:
                kwargs["status"] = False
        else:
            kwargs["status"] = False

        get_obj = self.get_by_id_obj(id)
        for key, value in kwargs.items():
            if key != "nfts":
                setattr(get_obj, key, value)
        _nfts = kwargs.get("nfts")
        if _nfts:
            if isinstance(_nfts, list):
                for nft in _nfts:
                    self.add_nft(get_obj, nft)
        db.session.commit()

    def get_by_id_obj(self, id):
        obj = self.query.filter_by(id=id).first()
        if not obj:
            return
        return obj

    def get_by_id(self, id):
        """Get a user by id"""
        obj = self.query.filter_by(id=id).first()
        if not obj:
            return
        obj = self.row2dict(obj)
        return obj

    def get_by_user_id(self, owner_id):
        """Get a user by id"""
        obj = self.query.filter_by(owner=owner_id).first()
        if not obj:
            return
        obj = self.row2dict(obj)
        return obj

# Webhook
# SetApprovalForAll
# Parameters: true