// MARK: - View

public struct {{ viewName }}: View {

    private let store: StoreOf<{{ featureName }}>

    public init(
        store: StoreOf<{{ featureName }}>
    ) {
        self.store = store
    }

    public var body: some View {
        WithViewStore(store) { viewStore in
            Text("{{ viewName }}")
        }
    }
}

// MARK: - Preview

public struct {{ viewName }}_Preview: PreviewProvider {

    public static var previews: some View {
        {{ viewName }}(store: StoreOf<{{ featureName }}>(
{%- if subReducerFeatures|length > 0 -%}
        initialState: .init(
 {%- for subFeatureKey, subFeatureValue in subReducerFeatures.items() %}
           {{ subFeatureValue.varName }}: {{ subFeatureValue.featureName }}.State(){{ ", " if not loop.last else "" }}
 {%- endfor %}
        )) {
{%- else -%}
            initialState: .init()) {
{%- endif %}
            {{ featureName }}()
        }
//             withDependencies: {
//                 $0.someDependency = something
//             }
        )
    }
}
