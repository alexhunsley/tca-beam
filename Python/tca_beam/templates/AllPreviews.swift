import SwiftUI
import ComposableArchitecture

// MARK: - Preview all feature Views in a VStack

public struct AllPreviews_Preview: PreviewProvider {

    public static var previews: some View {
        VStack {
            Spacer()
{%- for feature in allFeatures %}
            {{ feature.viewName }}(store: StoreOf<{{ feature.featureName }}>(
{%- if subReducerFeatures|length > 0 -%}
        initialState: .init(
 {%- for subFeatureKey, subFeatureValue in subReducerFeatures.items() %}
            {{ subFeatureValue.varName }}: {{ subFeatureValue.featureName }}.State(){{ ", " if not loop.last else "" }}
 {%- endfor %}
        )) {
{%- else -%}
            initialState: .init()) {
{%- endif %}
                {{ feature.featureName }}()
            }
//                 withDependencies: {
//                     $0.someDependency = something
//                 }
            )
            Spacer()
{%- endfor %}
       }
    }
}
