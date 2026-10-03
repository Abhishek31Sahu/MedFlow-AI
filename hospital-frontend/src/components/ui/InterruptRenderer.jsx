import BedRecommendationList from "./BedRecommendationList";
import PatientSelectionList from "./PatientSelectionList";

export default function InterruptRenderer({
  interrupt,
  onSelectBed,
  onSelectPatient,
}) {
  if (!interrupt) return null;

  switch (interrupt.type) {
    case "BED_SELECTION":
      return (
        <BedRecommendationList
          message={interrupt.message}
          recommendations={
            interrupt.recommended_beds || interrupt.recommendations
          }
          onSelect={onSelectBed}
        />
      );

    case "patient_selection":
      return (
        <PatientSelectionList
          patients={interrupt.patients}
          onSelect={onSelectPatient}
        />
      );

    default:
      return null;
  }
}
