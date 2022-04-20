from django import forms


class RentForm(forms.Form):
    name = forms.CharField(max_length=20)
    email = forms.EmailField()
    flat_type = forms.ChoiceField(choices=(("1", "1BHK"), ("2", "2BHK"), ("3", "3BHK")),
                                  widget=forms.RadioSelect)
    lease_type = forms.ChoiceField(choices=(("Family", "Family"), ("Company", "Company"), ("Bachelor", "Bachelor")),
                                   widget=forms.RadioSelect)
    furnishing = forms.ChoiceField(choices=(("Full", "Fully Furnished"), ("Partial", "Partially Furnished"),
                                            ("No", "Not Furnished")))
    amenities = forms.MultipleChoiceField(choices=(("1", "Gated community"),
                                                   ("2", "Pool"),
                                                   ("3", "Gym"),
                                                   ("4", "Parking"),
                                                   ("5", "Gas pipeline")),
                                          widget=forms.CheckboxSelectMultiple)


class BuyForm(forms.Form):
    name = forms.CharField(max_length=20)
    email = forms.EmailField()
    flat_type = forms.ChoiceField(choices=(("1", "1BHK"), ("2", "2BHK"), ("3", "3BHK")),
                                  widget=forms.RadioSelect)
    lease_type = forms.ChoiceField(choices=(("Family", "Family"), ("Company", "Company"),
                                            ("Bachelor", "Bachelor")),
                                   widget=forms.RadioSelect)
    purchase_type = forms.ChoiceField(choices=(("1", "Resale"), ("2", "New booking")),
                                      widget=forms.RadioSelect)
    avail_emi = forms.ChoiceField(choices=(("Yes", "Yes"), ("No", "No")), widget=forms.RadioSelect)
    amenities = forms.MultipleChoiceField(choices=(("1", "Gated community"),
                                                   ("2", "Pool"),
                                                   ("3", "Gym"),
                                                   ("4", "Parking"),
                                                   ("5", "Gas pipeline")),
                                          widget=forms.CheckboxSelectMultiple)
