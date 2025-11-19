from rest_framework import serializers
from .models import User
from lawyer.models import LawyerProfile
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.Serializer):
    """Serializer for User MongoEngine Document"""

    id = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    username = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    profile_picture = serializers.URLField(read_only=True)
    cover_photo = serializers.URLField(read_only=True)  # Added cover_photo
    auth_provider = serializers.CharField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    has_password = serializers.SerializerMethodField()
    
    def get_has_password(self, instance):
        return instance.password != '!'
    
    def to_representation(self, instance):
        """Convert MongoEngine document to dict"""
        return {
            'id': str(instance.id),
            'email': instance.email,
            'username': instance.username,
            'name': instance.name,
            'profile_picture': instance.profile_picture,
            'cover_photo': instance.cover_photo, # Added cover_photo
            'auth_provider': instance.auth_provider,
            'date_joined': instance.date_joined,
            'phone': instance.phone,
            'role': instance.role,
            'is_verified': instance.is_verified,
            'is_lawyer_verified': instance.is_lawyer_verified,
            'lawyer_verification_status': instance.lawyer_verification_status,
            'has_password': self.get_has_password(instance)
        }


class RegisterSerializer(serializers.Serializer):
    """Serializer for user registration"""

    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True, max_length=150)
    name = serializers.CharField(required=False, allow_blank=True, max_length=255)
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(
        choices=[("client", "Client"), ("lawyer", "Lawyer")], default="client"
    )
    phone = serializers.CharField(required=False, allow_blank=True, max_length=20)
    license_number = serializers.CharField(
        required=False, allow_blank=True, max_length=120
    )
    bar_council_id = serializers.CharField(
        required=False, allow_blank=True, max_length=120
    )
    education = serializers.CharField(required=False, allow_blank=True, max_length=255)
    experience_years = serializers.IntegerField(required=False, min_value=0)
    law_firm = serializers.CharField(required=False, allow_blank=True, max_length=255)
    specializations = serializers.ListField(
        child=serializers.CharField(max_length=120), required=False, allow_empty=True
    )
    consultation_fee = serializers.CharField(
        required=False, allow_blank=True, max_length=120
    )
    bio = serializers.CharField(required=False, allow_blank=True)
    verification_documents = serializers.ListField(
        child=serializers.CharField(max_length=512), required=False, allow_empty=True
    )

    def validate_email(self, value):
        """Check if email already exists"""
        if not value:
            raise serializers.ValidationError("Email address is required.")

        # Basic email format validation
        if "@" not in value or "." not in value.split("@")[-1]:
            raise serializers.ValidationError("Please enter a valid email address.")

        # Check if email already exists
        try:
            if User.objects(email=value).first():
                raise serializers.ValidationError(
                    "An account with this email already exists. Please use a different email or try logging in."
                )
        except Exception as e:
            if "already exists" in str(e):
                raise
            raise serializers.ValidationError(
                "Unable to validate email. Please try again."
            )

        return value.lower().strip()

    def validate_username(self, value):
        """Check if username already exists and validate format"""
        if not value:
            raise serializers.ValidationError("Username is required.")

        if len(value) < 3:
            raise serializers.ValidationError(
                "Username must be at least 3 characters long."
            )

        if len(value) > 150:
            raise serializers.ValidationError(
                "Username must not exceed 150 characters."
            )

        # Check for valid characters (alphanumeric, underscore, hyphen)
        import re

        if not re.match(r"^[a-zA-Z0-9_-]+$", value):
            raise serializers.ValidationError(
                "Username can only contain letters, numbers, underscores, and hyphens."
            )

        # Check if username already exists
        try:
            if User.objects(username=value).first():
                raise serializers.ValidationError(
                    "This username is already taken. Please choose a different username."
                )
        except Exception as e:
            if "already taken" in str(e):
                raise
            raise serializers.ValidationError(
                "Unable to validate username. Please try again."
            )

        return value.strip()

    def validate_specializations(self, value):
        if isinstance(value, str):
            items = [item.strip() for item in value.split(",") if item.strip()]
            return items
        return value or []

    def validate_verification_documents(self, value):
        if isinstance(value, str):
            items = [item.strip() for item in value.split(",") if item.strip()]
            return items
        return value or []

    def validate_experience_years(self, value):
        if value in (None, ""):
            return 0
        return value

    def validate(self, attrs):
        """Validate password match and lawyer-specific fields"""
        # Validate password match
        password = attrs.get("password", "")
        password2 = attrs.get("password2", "")
        errors = {}

        # Check if passwords are provided
        if not password or not password2:
            errors["password"] = "Password is required."
            raise serializers.ValidationError(errors)

        # Validate password strength using Django's validators FIRST
        # This will catch common passwords, numeric passwords, etc.
        password_validation_errors = []
        try:
            validate_password(password)
        except Exception as e:
            # Extract all password validation errors
            if hasattr(e, "messages"):
                password_validation_errors.extend(e.messages)
            else:
                password_validation_errors.append(str(e))

        # Additional password strength validation (minimum length)
        if len(password) < 8:
            password_validation_errors.append(
                "Password must be at least 8 characters long."
            )

        # Custom password strength checks
        import re

        if not re.search(r"[A-Z]", password):
            password_validation_errors.append(
                "Password must contain at least one uppercase letter."
            )

        if not re.search(r"[a-z]", password):
            password_validation_errors.append(
                "Password must contain at least one lowercase letter."
            )

        if not re.search(r"[0-9]", password):
            password_validation_errors.append(
                "Password must contain at least one number."
            )

        if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\;/`~]', password):
            password_validation_errors.append(
                "Password must contain at least one special character (!@#$%^&*etc.)."
            )

        # If there are password validation errors, set them
        if password_validation_errors:
            errors["password"] = " ".join(password_validation_errors)

        # Check if passwords match (separate error for password2 field)
        if password != password2:
            errors["password2"] = (
                "Passwords do not match. Please ensure both passwords are identical."
            )

        # If there are any password errors, raise them now
        if errors:
            raise serializers.ValidationError(errors)

        # Validate lawyer-specific fields
        role = attrs.get("role", "client")
        if role == "lawyer":
            missing_fields = []
            field_labels = {
                "license_number": "License Number",
                "bar_council_id": "Bar Council ID",
            }

            license_number = attrs.get("license_number", "").strip()
            bar_council_id = attrs.get("bar_council_id", "").strip()

            if not license_number:
                missing_fields.append("license_number")
            if not bar_council_id:
                missing_fields.append("bar_council_id")

            if missing_fields:
                error_dict = {}
                for field in missing_fields:
                    error_dict[field] = (
                        f"{field_labels[field]} is required for lawyer registration."
                    )
                raise serializers.ValidationError(error_dict)

        return attrs

    def create(self, validated_data):
        """Create new user"""
        validated_data.pop("password2")
        role = validated_data.pop("role", "client")
        phone = validated_data.pop("phone", "")
        license_number = validated_data.pop("license_number", "")
        bar_council_id = validated_data.pop("bar_council_id", "")
        education = validated_data.pop("education", "")
        experience_years = validated_data.pop("experience_years", 0)
        law_firm = validated_data.pop("law_firm", "")
        specializations = validated_data.pop("specializations", []) or []
        consultation_fee = validated_data.pop("consultation_fee", "")
        bio = validated_data.pop("bio", "")
        verification_documents = validated_data.pop("verification_documents", []) or []

        user = User.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            name=validated_data.get("name", ""),
            password=validated_data["password"],
            role=role,
            phone=phone,
        )

        if role == "lawyer":
            user.lawyer_verification_status = "pending"
            user.is_lawyer_verified = False
            user.save()
            LawyerProfile.objects(user=user).delete()
            LawyerProfile.objects.create(
                user=user,
                phone=phone,
                education=education,
                experience_years=experience_years or 0,
                law_firm=law_firm,
                specializations=specializations,
                license_number=license_number,
                bar_council_id=bar_council_id,
                consultation_fee=consultation_fee,
                bio=bio,
                verification_documents=verification_documents,
                verification_status="pending",
            )
        else:
            user.lawyer_verification_status = "not_applicable"
            user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        error_messages={
            "required": "Email address is required.",
            "invalid": "Please enter a valid email address.",
        },
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        error_messages={
            "required": "Password is required.",
            "blank": "Password cannot be empty.",
        },
    )

    def validate_email(self, value):
        """Validate and normalize email"""
        if not value:
            raise serializers.ValidationError("Email address is required.")
        return value.lower().strip()

    def validate_password(self, value):
        """Validate password is not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError("Password is required.")
        return value


class GoogleAuthSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp_code = serializers.CharField(required=True, max_length=6, min_length=6)


class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class UserProfileSerializer(serializers.Serializer):
    """Serializer for updating user profile"""

    name = serializers.CharField(required=False, allow_blank=True, max_length=255)
    profile_picture = serializers.URLField(required=False, allow_blank=True, max_length=255)
    cover_photo = serializers.URLField(required=False, allow_blank=True, max_length=255) # Added cover_photo
    role = serializers.CharField(read_only=True)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.profile_picture = validated_data.get(
            "profile_picture", instance.profile_picture
        )
        instance.cover_photo = validated_data.get(
            "cover_photo", instance.cover_photo
        )  # Added cover_photo
        instance.save()
        return instance

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp_code = serializers.CharField(required=True, max_length=6, min_length=6)
    new_password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        """Validate password match"""
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Password fields didn't match."}
            )
        return attrs

class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change"""
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "New passwords didn't match."})
        return attrs

class AddPasswordSerializer(serializers.Serializer):
    """Serializer for adding a password to a Google-authenticated user"""
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "New passwords didn't match."})
        return attrs


class ChatMessageSerializer(serializers.Serializer):
    """Serializer for chat messages"""

    id = serializers.CharField(read_only=True)
    sender = serializers.SerializerMethodField()
    message = serializers.CharField()
    message_type = serializers.CharField()
    document_id = serializers.CharField(allow_blank=True)
    document_title = serializers.CharField(allow_blank=True)
    is_read = serializers.BooleanField()
    created_at = serializers.DateTimeField()

    def get_sender(self, obj):
        from .models import User

        try:
            # Try to get sender attributes directly
            if hasattr(obj, 'sender') and obj.sender:
                sender = obj.sender
                if hasattr(sender, 'id'):
                    return {
                        'id': str(sender.id),
                        'name': sender.name or sender.username or 'Unknown',
                        'username': sender.username or 'unknown',
                    }
            if hasattr(obj, 'sender_id') and obj.sender_id:
                sender = User.objects(id=obj.sender_id).first()
                if sender:
                    return {
                        'id': str(sender.id),
                        'name': sender.name or sender.username or 'Unknown',
                        'username': sender.username or 'unknown',
                    }
        except Exception as e:
            print(f"Error getting sender: {e}")
        return {'id': 'unknown', 'name': 'Unknown', 'username': 'unknown'}

    def to_representation(self, instance):
        """Ensure keys serialize cleanly"""

        data = super().to_representation(instance)
        result = {}
        for key, value in data.items():
            key = str(key)
            if hasattr(value, 'isoformat'):
                result[key] = value.isoformat() if value else None
            elif isinstance(value, dict):
                result[key] = {str(nested_key): nested_value for nested_key, nested_value in value.items()}
            else:
                result[key] = value
        return result


class ChatConversationSerializer(serializers.Serializer):
    """Serializer for chat conversations"""

    id = serializers.CharField(read_only=True)
    connection_request_id = serializers.SerializerMethodField()
    client = serializers.SerializerMethodField()
    lawyer = serializers.SerializerMethodField()
    is_active = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    def _serialize_user(self, user):
        if not user:
            return {'id': 'unknown', 'name': 'Unknown', 'username': 'unknown'}
        return {
            'id': str(user.id),
            'name': user.name or user.username or 'Unknown',
            'username': user.username or 'unknown',
        }

    def get_client(self, obj):
        return self._serialize_user(getattr(obj, 'client', None))

    def get_lawyer(self, obj):
        return self._serialize_user(getattr(obj, 'lawyer', None))

    def get_connection_request_id(self, obj):
        connection_request = getattr(obj, 'connection_request', None)
        return str(connection_request.id) if connection_request else None

    def get_last_message(self, obj):
        from .models import ChatMessage

        try:
            last_message = ChatMessage.objects(conversation=obj).order_by('-created_at').first()
            if last_message:
                serializer = ChatMessageSerializer(last_message, context=self.context)
                return serializer.data
        except Exception as exc:
            print(f"Error fetching last message for conversation {obj.id}: {exc}")
        return None

    def get_unread_count(self, obj):
        from .models import ChatMessage

        try:
            queryset = ChatMessage.objects(conversation=obj, is_read=False)
            request = self.context.get('request') if hasattr(self, 'context') else None
            if request and getattr(request, 'user', None):
                user_id = str(request.user.id)
                return sum(1 for message in queryset if str(message.sender.id) != user_id)
            return queryset.count()
        except Exception as exc:
            print(f"Error calculating unread count for conversation {obj.id}: {exc}")
            return 0

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = str(getattr(instance, 'id', data.get('id')))
        data['created_at'] = (
            instance.created_at.isoformat() if getattr(instance, 'created_at', None) else None
        )
        data['updated_at'] = (
            instance.updated_at.isoformat() if getattr(instance, 'updated_at', None) else None
        )
        return data


class LawyerConnectionStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=['accepted', 'declined'])
    message = serializers.CharField(required=False, allow_blank=True)


