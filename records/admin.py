from django.contrib import admin
from .models import PatientRecord, Prescription
# Inline Admin for Prescriptions
class PrescriptionInline(admin.TabularInline):
    model = Prescription
    extra = 1 # Number of empty forms to display

# Admin for PatientRecord Model
@admin.register(PatientRecord)
class PatientRecordAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', # Corrected: 'full_name' is a direct field on PatientRecord
        'age', 
        'gender', 
        'patient', # Displays the __str__ of the CustomUser (email)
        'doctor',  # Displays the __str__ of the CustomUser (email)
        'visit_date', 
        'follow_up_date'
    )
    list_filter = (
        'gender', 
        'visit_date', 
        'patient__hospital', 
        'doctor__hospital',
        # You could also filter by the patient's email if desired:
        # 'patient__email', 
        # 'doctor__email',
    )
    search_fields = (
        'full_name', 
        'diagnosis', 
        'patient__email',  # Correct: searching by related CustomUser's email
        'doctor__email',   # Correct: searching by related CustomUser's email
    )
    date_hierarchy = 'visit_date'
    ordering = ('-visit_date',)
    inlines = [PrescriptionInline]

    # Customize the form layout for better organization
    fieldsets = (
        (None, {'fields': ('patient', 'doctor')}),
        ('Patient Details', {
            'fields': ('full_name', 'age', 'gender') # Corrected: 'full_name' instead of 'email'
        }),
        ('Medical Information', {
            'fields': ('diagnosis', 'treatment_plan', 'notes'),
            'classes': ('collapse',), # Makes this section collapsible
        }),
        ('Vital Signs', {
            'fields': ('blood_pressure', 'temperature', 'pulse_rate'),
            'classes': ('collapse',),
        }),
        ('Dates', {'fields': ('visit_date', 'follow_up_date')}),
    )

    # Limit choices for 'patient' and 'doctor' in the admin form
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        from accounts.models import CustomUser # Import CustomUser here if it's not at the top
        if db_field.name == "patient":
            kwargs["queryset"] = CustomUser.objects.filter(roles='patient')
        if db_field.name == "doctor":
            kwargs["queryset"] = CustomUser.objects.filter(roles='doctor')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Admin for Prescription Model (optional, as it's an inline)
@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('record', 'drug_name', 'dosage', 'frequency', 'duration',)
    list_filter = (
        'record__full_name', # Corrected: filter by the patient's full_name on the PatientRecord
        # Alternatively, if you want to filter by the patient's email linked to the record:
        # 'record__patient__email', 
        'drug_name', # You can filter by drug name too
    )
    search_fields = ('drug_name', 'record__full_name',) # Corrected: searching by patient's full_name on the record