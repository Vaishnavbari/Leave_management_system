from rest_framework import serializers
from .models import LeaveType, LeaveRule, Leave
from datetime  import datetime, timedelta


class LeaveTypeSerializer(serializers.ModelSerializer):
    type = serializers.CharField()
    description = serializers.CharField()

    class Meta:
        model = LeaveType
        fields = ["type", "description"]

    def validate(self, validated_data):
        type = validated_data.get("type")
        leave_type = LeaveType.objects.filter(type=type)
        if leave_type.exists():
            raise serializers.ValidationError("Leave type already exists")
        
        return super().validate(validated_data)

    def create(self, validated_data):
        type = validated_data.get("type")
        description = validated_data.get("description")
        leave_type = LeaveType.objects.create(type=type, description=description)
        return leave_type
    
    def update(self, instance, validated_data):
        instance.type = validated_data.get("type", instance.type)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        return instance
    

class LeaveRuleSerializer(serializers.ModelSerializer):
    validity = serializers.IntegerField()
    class Meta:
        model = LeaveRule
        fields = ["validity", "leave_type", "role"]

    def validate(self, validated_data):
        leave_type = validated_data.get("leave_type")
        role = validated_data.get("role")

        leave_rule = LeaveRule.objects.filter(leave_type=leave_type, role=role)
        if leave_rule.exists():
            raise serializers.ValidationError("Leave rule already exists")
        
        return super().validate(validated_data)

    def create(self, validated_data):
        validity = validated_data.get("validity")
        leave_type = validated_data.get("leave_type")
        role = validated_data.get("role")
        leave_type = LeaveRule.objects.create(validity=validity, leave_type=leave_type, role=role)
        return leave_type
    
    def update(self, instance, validated_data):
        instance.validity = validated_data.get("validity", instance.validity)
        instance.leave_type = validated_data.get("leave_type", instance.leave_type)
        instance.role = validated_data.get("role", instance.role)
        instance.save()
        return instance


class LeaveSerializer(serializers.ModelSerializer):
   date_from = serializers.DateField()
   date_to = serializers.DateField()
   reason = serializers.CharField()   
   class Meta:
       model = Leave
       fields = ["leave_type", "date_from", "date_to", "reason"]
    
   def validate(self, validated_data):
       user = self.context.get("user")
       leave_type = validated_data.get("leave_type")
       date_from = validated_data.get("date_from")
       date_to = validated_data.get("date_to")

    #    if self.instance:
    #        date_from = validated_data.get("date_from") if validated_data.get("date_from") else self.instance.date_from 
    #        date_to = validated_data.get("date_to") if validated_data.get("date_to") else self.instance.date_to
    #        leave_type = validated_data.get("leave_type") if validated_data.get("leave_type") else self.instance.leave_type
    #        reason = validated_data.get("reason") if validated_data.get("reason") else self.instance.reason
         
       if date_from <= datetime.now().date():
           raise serializers.ValidationError("Date-from should be greater than today's date")
       
       if date_from >= date_to:
           raise serializers.ValidationError("Date-to should be greater than date-from")
       
       # check leave rule validation 
       leave_rule = LeaveRule.objects.filter(leave_type=leave_type, role=user.role.id, status=True).first()

       # Leave rule Validity   
       validity = leave_rule.validity

       current_date = datetime.now().date()

       # count days between days from and date to     
       count_days_between = date_from - current_date

       if not count_days_between.days > validity:
           raise serializers.ValidationError(f"You applied this leave before {validity} days ")   
          
       return super().validate(validated_data)

   def create(self, validated_data):
       user = self.context.get("user")
       leave_type = validated_data.get("leave_type")
       date_from = validated_data.get("date_from")
       date_to = validated_data.get("date_to")
       reason = validated_data.get("reason")
       leave = Leave.objects.create(leave_type=leave_type, date_from=date_from, date_to=date_to, reason=reason, user=user)
       return leave
   
#    def update(self, instance, validated_data):
#         instance.leave_type = validated_data.get("leave_type", instance.leave_type)
#         instance.date_from = validated_data.get("date_from", instance.date_from)
#         instance.date_to = validated_data.get("date_to", instance.date_to)
#         instance.reason = validated_data.get("reason", instance.reason)
#         instance.save()
#         return instance